pipeline {
    agent any
    parameters {
        string(name: 'SERVER_NAME', defaultValue: 'Server_Portugal', description: 'Friendly name of the server')
        string(name: 'SERVER_IP', defaultValue: '192.168.1.19', description: 'IP address of the server')
    }
    stages {
        /*
        stage('Checkout Repository') {
            steps {
                git 'https://github.com/RodrigoDBraga/AnsibleTest'
            }
        }
        
        stage('Fetch IP and Institution Name') {
            steps {
                script {
                    def output = sh(script: "python3 scripts/get_ip_and_name.py", returnStdout: true).trim()
                    def (server_ip, server_name) = output.split(',')
                    env.SERVER_IP = server_ip
                    env.SERVER_NAME = server_name
                }
            }
        }*/
        stage('Fetch IP Address') {
            steps {
                script {
                    def ip_address = sh(script: "hostname -I | awk '{print \$1}'", returnStdout: true).trim()
                    if (ip_address == '172.17.0.2') {
                        ip_address = '192.168.1.19'
                    }
                    env.SERVER_IP = ip_address
                    echo "Fetched IP: ${env.SERVER_IP}"
                }
            }
        }
        /*
        stage('Send IP to Monitoring Server') {
            steps {
                script {
                    // Replace with the actual URL of your monitoring server
                    def monitoring_server_url = "http://your-monitoring-server.com/api/receive_ip" //still need to change this ip
                    sh "curl -X POST ${monitoring_server_url} -d 'ip=${env.SERVER_IP}'"
                }
            }
        }
        */

        stage('Run Ansible Playbook') {
            steps {
                echo "Fetched IP: ${env.SERVER_IP}"
                /*
                ansiblePlaybook(
                    playbook: 'playbooks/playbook.yml',
                    inventory: 'playbooks/inventory.ini',
                    extras: '--extra-vars "server_name=${env.SERVER_NAME} server_ip=${env.SERVER_IP}"'
                    //extras: '--extra-vars "server_ip=${env.SERVER_IP}"'
                )
                */
                /*ansiblePlaybook(
                    playbook: 'playbooks/playbook.yml',
                    inventory: 'playbooks/inventory.ini'
                )*/
                //$ ansible-playbook playbooks/playbook.yml -i playbooks/inventory.ini --extra-vars server_ip=${env.SERVER_IP}
                withEnv(["PATH+ANSIBLE=/usr/local/bin"]) {
                    sh 'echo $PATH'
                    sh 'which ansible-playbook'
                    ansiblePlaybook(
                        playbook: 'playbooks/playbook.yml',
                        inventory: 'playbooks/inventory.ini',
                        extras: '--extra-vars "server_ip=${env.SERVER_IP}"'
                    )
                }
                echo "Fetched IP: ${env.SERVER_IP}"
            }
        }
        stage('Copy to DigitalOcean Machine') {
            steps {
                sshagent(['DigitalOceanSSHKey']) {
                    sh 'scp -r * root@209.97.183.9:/home/iprolepsis/monitoring'
                }
            }
        }
        stage('Execute Docker-Compose Command') {
            steps {
                sshagent(['DigitalOceanSSHKey']) {
                    sh 'ssh root@209.97.183.9 "cd /home/iprolepsis/monitoring && docker-compose up -d"'
                }
            }
        }
    }
}