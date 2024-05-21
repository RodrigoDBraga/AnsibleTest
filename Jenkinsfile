pipeline {
    agent any
    parameters {
        string(name: 'SERVER_NAME', defaultValue: 'Server_Portugal', description: 'Friendly name of the server')
        string(name: 'SERVER_IP', defaultValue: '192.168.1.19', description: 'IP address of the server')
    }
    stages {
        stage('Navigate to Local Repository') {
            steps {
                dir('E:/Programas/IT/Git/changed-monitoring-main') {
                    echo "Navigated to local repository"
                }
            }
        }
        stage('Update Configuration') {
            steps {
                dir('E:/Programas/IT/Git/changed-monitoring-main') {
                    script {
                        def configFilePath = 'monitoring-main/client/configs/otel-collector-config.yaml'
                        def config = readFile configFilePath
                        config = config.replace("{SERVER_IP}", params.SERVER_IP)
                        writeFile file: configFilePath, text: config
                    }
                }
            }
        }
        stage('Copy to DigitalOcean Machine') {
            steps {
                dir('E:/Programas/IT/Git/changed-monitoring-main') {
                    sshagent(['DigitalOceanSSHKey']) {
                        sh 'scp -r * root@209.97.183.9:/home/iprolepsis/monitoring'
                    }
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