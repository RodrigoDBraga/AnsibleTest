import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

# Configuration
LOKI_URL = "http://localhost:3100"
PROMETHEUS_URL = "http://localhost:9090"
CLIENT_SERVERS = ["209.97.134.226:9100", "142.93.38.159:9100"]
REPORT_DURATION = timedelta(hours=6)  # Can be changed to timedelta(days=90) for 3 months
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ServerReports")

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Metrics configuration
METRICS = {
    "cpu_usage": {
        "query": '100 - (avg by(instance) (rate(node_cpu_seconds_total{{instance="{}",mode="idle"}}[1m])) * 100)',
        "unit": "%",
        "title": "CPU Usage"
    },
    "memory_usage": {
        "query": '(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100',
        "unit": "%",
        "title": "Memory Usage"
    },
    "disk_space_usage": {
        "query": '100 - ((node_filesystem_avail_bytes{{mountpoint="/"}} * 100) / node_filesystem_size_bytes{{mountpoint="/"}})',
        "unit": "%",
        "title": "Disk Space Usage"
    },
    "disk_io": {
        "query": 'rate(node_disk_io_time_seconds_total[5m])',
        "unit": "ops/sec",
        "title": "Disk I/O"
    },
    "network_throughput": {
        "query": '(sum by(instance) (rate(node_network_transmit_bytes_total[5m]) + rate(node_network_receive_bytes_total[5m]))) / 1024 / 1024',
        "unit": "MB/s",
        "title": "Network Throughput"
    },
    "network_error_rate": {
        "query": '(sum by(instance) (rate(node_network_transmit_errs_total[5m]) + rate(node_network_receive_errs_total[5m]))) / (sum by(instance) (rate(node_network_transmit_packets_total[5m]) + rate(node_network_receive_packets_total[5m]))) * 100',
        "unit": "%",
        "title": "Network Error Rate"
    },
    "service_availability": {
        "query": 'avg_over_time(up{{job="node"}}[5m]) * 100',
        "unit": "%",
        "title": "Service Availability"
    },
    "response_time": {
        "query": 'histogram_quantile(0.95, sum(rate(node_scrape_collector_duration_seconds_bucket[5m])) by (le, instance))',
        "unit": "seconds",
        "title": "95th Percentile Response Time"
    }
}

def query_prometheus(query, start_time, end_time):
    url = f"{PROMETHEUS_URL}/api/v1/query_range"
    params = {
        'query': query,
        'start': start_time.isoformat("T") + "Z",
        'end': end_time.isoformat("T") + "Z",
        'step': '5m'  # 5-minute resolution for longer periods
    }
    response = requests.get(url, params=params)
    return response.json()

def query_loki(query, start_time, end_time):
    url = f"{LOKI_URL}/loki/api/v1/query_range"
    params = {
        'query': query,
        'start': start_time.isoformat("T") + "Z",
        'end': end_time.isoformat("T") + "Z",
        'limit': 1000  # Increased limit
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error querying Loki: {response.status_code} - {response.text}")
    return response.json()

def plot_metric(df, metric_name, server, unit):
    plt.figure(figsize=(16, 8))
    df['value'].plot(linewidth=0.5)
    plt.title(f"{METRICS[metric_name]['title']} for {server} over {REPORT_DURATION}")
    plt.ylabel(f"{METRICS[metric_name]['title']} ({unit})")
    plt.xlabel("Time")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Highlight max points
    max_points = get_spaced_max_values(df, 5, timedelta(hours=24))
    plt.scatter(max_points.index, max_points['value'], color='red', zorder=5, label='Top 5 Max Values (24h apart)')
    
    for idx, row in max_points.iterrows():
        plt.annotate(f"{row['value']:.3f}", (idx, row['value']), textcoords="offset points", xytext=(0,10), ha='center')

    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{server.replace(':', '_')}_{metric_name}.png", dpi=300)
    plt.close()

def get_spaced_max_values(df, n=5, min_interval=timedelta(hours=24)):
    max_values = []
    last_timestamp = df.index.min() - min_interval
    sorted_df = df.sort_values('value', ascending=False)
    
    for idx, row in sorted_df.iterrows():
        if idx - last_timestamp >= min_interval:
            max_values.append(row)
            last_timestamp = idx
        if len(max_values) == n:
            break
    
    return pd.DataFrame(max_values)

def get_alert_periods(df, alert_threshold):
    df['alert'] = df['value'] > alert_threshold
    alert_periods = []
    alert_start = None
    for index, row in df.iterrows():
        if row['alert'] and alert_start is None:
            alert_start = index
        elif not row['alert'] and alert_start is not None:
            alert_periods.append((alert_start, index, df.loc[alert_start:index, 'value'].max()))
            alert_start = None
    if alert_start is not None:
        alert_periods.append((alert_start, df.index[-1], df.loc[alert_start:, 'value'].max()))
    return alert_periods

#def query_alerts(start_time, end_time):
#    query = 'ALERTS{alertstate="firing"}'
#    return query_prometheus(query, start_time, end_time)

def query_alerts(start_time, end_time):
    query = 'ALERTS{alertstate="firing"}'
    # Use a step size that matches the alert evaluation interval
    step = '15s'  # Assuming the alert evaluation interval is 15 seconds
    url = f"{PROMETHEUS_URL}/api/v1/query_range"
    params = {
        'query': query,
        'start': start_time.isoformat("T") + "Z",
        'end': end_time.isoformat("T") + "Z",
        'step': step
    }
    response = requests.get(url, params=params)
    return response.json()


def process_alerts(alert_data):
    alert_occurrences = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    for result in alert_data['data']['result']:
        alert_name = result['metric']['alertname']
        severity = result['metric'].get('severity', 'unknown')
        
        for timestamp, value in result['values']:
            if float(value) == 1:  # Alert is firing
                date = datetime.fromtimestamp(timestamp).date()
                alert_occurrences[alert_name][date][severity] += 1
    
    return alert_occurrences

def generate_report(server):
    end_time = datetime.now()
    start_time = end_time - REPORT_DURATION
    timestamp = end_time.strftime("%Y%m%d_%H%M%S")

    print(f"Generating report for {server}")

    report_filename = f"{server.replace(':', '_')}_report_{timestamp}.txt"
    with open(os.path.join(OUTPUT_DIR, report_filename), "w") as f:
        f.write(f"Report for {server}\n")
        f.write(f"Duration: {REPORT_DURATION}\n")
        f.write(f"From: {start_time} To: {end_time}\n\n")

        for metric_name, metric_info in METRICS.items():
            query = metric_info['query'].format(server)
            data = query_prometheus(query, start_time, end_time)

            if not data['data']['result']:
                f.write(f"No {metric_info['title']} data available. Check if the server is reachable and exporting metrics.\n\n")
                continue

            df = pd.DataFrame(data['data']['result'][0]['values'], columns=['timestamp', 'value'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('timestamp', inplace=True)
            df['value'] = df['value'].astype(float)

            avg_value = df['value'].mean()
            max_value = df['value'].max()

            f.write(f"{metric_info['title']}:\n")
            f.write(f"Average: {avg_value:.3f} {metric_info['unit']}\n")
            f.write(f"Maximum: {max_value:.3f} {metric_info['unit']}\n")

            spaced_max_values = get_spaced_max_values(df, 5, timedelta(hours=24))
            f.write("Top 5 Maximum Values (at least 24 hours apart):\n")
            for idx, row in spaced_max_values.iterrows():
                f.write(f"  {idx}: {row['value']:.3f} {metric_info['unit']}\n")

            # You would need to define appropriate alert thresholds for each metric
            #alert_threshold = 90 if metric_name == 'cpu_usage' else 80  # Example threshold
            alert_threshold = 0.7 if metric_name == 'network_throughput' else 0.01 if metric_name in ['network_error_rate', 'response_time'] else 99 if metric_name == 'service_availability' else 80 
            alert_periods = get_alert_periods(df, alert_threshold)
            if alert_periods:
                f.write(f"Alert Periods (threshold: {alert_threshold} {metric_info['unit']}):\n")
                for start, end, max_val in alert_periods:
                    f.write(f"  {start} to {end}: Max value {max_val:.3f} {metric_info['unit']}\n")
            else:
                f.write(f"No alerts triggered (threshold: {alert_threshold} {metric_info['unit']})\n")

            f.write("\n")

            plot_metric(df, metric_name, server, metric_info['unit'])

        # Query and process alerts
        alert_data = query_alerts(start_time, end_time)
        alert_occurrences = process_alerts(alert_data)
        
        f.write("Alert Summary:\n")
        for alert_name, dates in alert_occurrences.items():
            total_occurrences = sum(sum(severities.values()) for severities in dates.values())
            total_critical = sum(severities.get('critical', 0) for severities in dates.values())
            total_warning = sum(severities.get('warning', 0) for severities in dates.values())
            
            f.write(f"  {alert_name}:\n")
            f.write(f"    Total Occurrences: {total_occurrences}")
            #f.write(f"    Total Occurrences: {len(dates)}")
            #f.write(f"    This is dates: {dates}")
            if total_critical > 0:
                f.write(f", {total_critical} critical")
            if total_warning > 0:
                f.write(f", {total_warning} warning")
            f.write("\n")
            
            f.write("    Triggered on: ")
            triggered_days = []
            for date, severities in sorted(dates.items()):
                day_total = sum(severities.values())
                severity = 'critical' if severities.get('critical', 0) > 0 else 'warning'
                triggered_days.append(f"{date} ({severity}, {day_total})")
            f.write(", ".join(triggered_days))
            f.write("\n\n")

        # Query logs
        log_query = '{job =~".+"}'
        log_data = query_loki(log_query, start_time, end_time)

        f.write("Logs:\n")
        if 'result' in log_data['data'] and log_data['data']['result']:
            for stream in log_data['data']['result']:
                for value in stream['values']:
                    timestamp = datetime.fromtimestamp(float(value[0]) / 1e9).isoformat()
                    log_entry = value[1]
                    f.write(f"{timestamp} - {log_entry}\n")
        else:
            f.write("No logs found for this period.\n")

    print(f"Report generated for {server}")

# Generate reports for each server
for server in CLIENT_SERVERS:
    generate_report(server)

print("All reports generated.")
