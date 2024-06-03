pipeline {
    agent any

    
    
    stages {
        stage('Fetch IP Address') {
            steps {
                script {
                    def host_ip = sh(script: "ip route get 1 | awk '{print \$(NF-2); exit}'", returnStdout: true).trim()
                    env.SERVER_IP = host_ip
                    echo "Fetched IP: ${env.SERVER_IP}"
                }
            }
        }
        /*
        stage('Fetch IP Address') {
            steps {
                
                script {
                    def ip_address = sh(script: "hostname -I | awk '{print \$1}'", returnStdout: true).trim() // this is currently getting the docker/jenkins ip and not the machine itself
                    if (ip_address == '172.17.0.2') {
                        ip_address = '192.168.1.19'
                    }
                    env.SERVER_IP = ip_address
                    echo "Fetched IP: ${env.SERVER_IP}"
                    //env.SERVER_NAME = server_name
                    //echo "this is server_name: ${env.SERVER_NAME}"
                    //this is where we should run through the excel file and get the names from based on the ips, if an ip isn't on the list this all should still work but the name displayed should be the ip instead of a custom name

            }
        }
        }*/
       
        stage('Run Ansible Playbook') {
            steps {
                
                ansiblePlaybook(
                            playbook: 'playbooks/playbook.yml',
                            inventory: 'playbooks/inventory.ini',
                            extras: '--extra-vars "server_ip=${env.SERVER_IP} server_name=$(env.SERVER_NAME) " -vvvv ' 
                             
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