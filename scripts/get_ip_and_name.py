import socket
import pandas as pd

def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_institution_name(ip):
    df = pd.read_excel('iPROLEPSIS_IntegrationMatrix.xlsx')
    row = df[df['ip'] == ip]
    if not row.empty:
        return row.iloc[0]['name']
    return 'Unknown'

if __name__ == '__main__':
    ip_address = get_ip()
    institution_name = get_institution_name(ip_address)
    print(f"{ip_address},{institution_name}")