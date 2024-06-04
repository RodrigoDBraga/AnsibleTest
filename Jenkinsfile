pipeline {
    agent any

    /*
    environment {
        //SERVER_IP = ''
        SERVER_NAME = 'friendly_server_name' // Adjust as necessary
    }*/
    

    stages {   
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/RodrigoDBraga/AnsibleTest'
            }
        }
        stage('Install Ansible') {
            steps {
                sh '''
                    sudo apt update
                    sudo apt install -y ansible
                '''
            }
        }

        stage('Ensure Docker Permissions') {
            steps {
                script {
                    try {
                        sh 'docker ps -q'
                    } catch (Exception e) {
                        error('Jenkins user does not have permission to interact with Docker. Ensure the Jenkins user is in the Docker group and restart the Jenkins service.')
                    }
                }
            }
        }

        stage('Get Docker Container IPs') {
            steps {
                script {
                    def containerIps = sh(script: '''
                        docker ps -q | xargs -I {} docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' {}
                    ''', returnStdout: true).trim().split('\n')
                    def inventoryContent = '[Monitoring]\n'
                    for (ip in containerIps) {
                        inventoryContent += "${ip} ansible_user=root\n"
                    }
                    writeFile file: 'playbooks/inventory.ini', text: inventoryContent
                }
            }
        }


        stage('Run Ansible Playbook') {
            steps {
                    /*
                    sh '''
                        ansible-playbook -i playbooks/playbook.yml playbooks/inventory.ini 
                    '''
                    */
                    sh '''
                        ansible-playbook playbooks/playbook.yml -i playbooks/inventory.ini 
                    '''
                
            }
        }
    }
        /*     
        stage('Fetch IP Address') {
            steps {
                
                script {
                    def ip_address = sh(script: "hostname -I | awk '{print \$1}'", returnStdout: true).trim() // this is currently getting the docker/jenkins ip and not the machine itself
                    
                    env.SERVER_IP = ip_address
                    echo "Fetched IP: ${env.SERVER_IP}"
                    //env.SERVER_NAME = server_name
                    //echo "this is server_name: ${env.SERVER_NAME}"
                    //this is where we should run through the excel file and get the names from based on the ips, if an ip isn't on the list this all should still work but the name displayed should be the ip instead of a custom name

            }
        }
        }*/
       /*
        stage('Run Ansible Playbook') {
            steps {
                echo "Fetched IP: ${env.SERVER_IP}"
                echo "Host name: ${env.SERVER_NAME}"
                sh """
                ansible-playbook playbooks/playbook.yml playbooks/inventory.ini \
                    --extra-vars "server_ip='${SERVER_IP}'" \
                    --extra-vars "server_name='${SERVER_NAME}'" \
                    -vvvv 
                """ 
            }
        }*/


        /*
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
        }*/
    //}
}