pipeline {
    agent any

    
    
    stages {
        /*
        stage('Install Packages') {
            steps {
                ansiblePlaybook(
                    playbook: 'playbooks/install_packages.yml',
                    inventory: 'playbooks/inventory_file'
                )
            }
        }*/


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
        }
       
        stage('Run Ansible Playbook') {
            steps {
                /*
                script {
                def computerUser = sh(script: 'logname', returnStdout: true).trim()
                }
                */
                echo "2"
                

                
                echo "3"
                //echo "server_ip=\${env.SERVER_IP} server_name=\$(env.SERVER_NAME)"
                
                ansiblePlaybook(
                            playbook: 'playbooks/playbook.yml',
                            inventory: 'playbooks/inventory.ini',//,
                            extras: '--extra-vars "server_ip=${env.SERVER_IP} server_name=$(env.SERVER_NAME) " -vvvv ' // can also put here the server_name depending on what we are doing
                             
                )//.exec("-l") inside the extra-vars -->ansible_user=${computerUser}
                
                //sh 'ansible-playbook -i "localhost," -c local playbooks/playbook.yml  playbooks/inventory.ini ---extra-vars "server_ip=${env.SERVER_IP} server_name=$(env.SERVER_NAME) ansible_user=$USER" -vvvv'
                
                //ansiblePlaybook installation: 'Ansible', inventory: '/var/jenkins_home/workspace/Private_github_test/playbooks/inventory.ini', playbook: '/var/jenkins_home/workspace/Private_github_test/playbooks/playbook.yml', vaultTmpPath: ''
                
                echo "4"
                
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