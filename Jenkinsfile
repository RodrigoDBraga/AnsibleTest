pipeline {
    agent any
    parameters {
        string(name: 'SERVER_NAME', defaultValue: 'Server_Portugal', description: 'Friendly name of the server')
        string(name: 'SERVER_IP', defaultValue: '192.168.1.19', description: 'IP address of the server')
    }
    stages {
        stage('Checkout Repository') {
            steps {
                git 'https://github.com/RodrigoDBraga/AnsibleTest.git'
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
        }
        stage('Run Ansible Playbook') {
            steps {
                ansiblePlaybook(
                    playbook: 'playbooks/playbook.yml',
                    inventory: 'playbooks/inventory.ini',
                    extras: '--extra-vars "server_name=${env.SERVER_NAME} server_ip=${env.SERVER_IP}"'
                )
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