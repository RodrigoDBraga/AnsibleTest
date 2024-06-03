pipeline {
    agent any

    /*
    parameters {
        string(name: 'SERVER_NAME', defaultValue: 'Server_Portugal', description: 'Friendly name of the server')
        string(name: 'SERVER_IP', defaultValue: '192.168.1.19', description: 'IP address of the server')
    }
    */
    /*
    stages {
        stage('Install Packages') {
            steps {
                ansiblePlaybook(
                    playbook: 'playbooks/install_packages.yml',
                    inventory: 'playbooks/inventory_file'
                )
            }
        }
        */


        /*
        stage('Check User and Sudo Permissions') {
            steps {
                script {
                    // Check the current user
                    def currentUser = sh(script: 'whoami', returnStdout: true).trim()
                    echo "What user am I: ${currentUser}"

                    // Check if sudo is available
                    def sudoCheck = sh(script: '''
                        if command -v sudo &> /dev/null; then
                            sudo -n true 2>/dev/null && echo "has_sudo" || echo "no_sudo"
                        else
                            echo "no_sudo_command"
                        fi
                    ''', returnStdout: true).trim()

                    if (sudoCheck == "has_sudo") {
                        echo "User has sudo permissions."
                    } else if (sudoCheck == "no_sudo_command") {
                        echo "Sudo command is not available."
                    } else {
                        echo "User does not have sudo permissions."
                    }
                }
            }
        }

        stage('Attempt to Install Packages') {
            when {
                expression {
                    def sudoCheck = sh(script: '''
                        if command -v sudo &> /dev/null; then
                            sudo -n true 2>/dev/null && echo "has_sudo" || echo "no_sudo"
                        else
                            echo "no_sudo_command"
                        fi
                    ''', returnStdout: true).trim()
                    return sudoCheck == "has_sudo"
                }
            }
            steps {
                script {
                    // Install necessary packages
                    sh '''
                        sudo apt-get update
                        sudo apt-get install -y git docker.io docker-compose
                    '''
                }
            }
        }*/



        
        stage('Prepare Environment') {
            steps {
                script {
                    // Check if ansible is installed
                    def ansibleCheck = sh(script: 'which ansible-playbook', returnStatus: true)
                    steps {
                    sh 'apt-get update'
                    sh 'apt-get install -y ansible'
                    }
                    if (ansibleCheck != 0) {
                        // Ansible not found, attempt to install it
                        sh 'sudo apt-get update'
                        sh 'sudo apt-get install -y ansible'
                    }
                }
            }
        }
        
        
        /*
        stage('Checkout Repository') {
            steps {
                git 'https://github.com/RodrigoDBraga/AnsibleTest'
            }
        }
        */
        /*
        stage('Install sudo') {
            steps {
                ansiblePlaybook(
                    playbook: 'playbooks/install_sudo.yml',
                    inventory: 'playbooks/inventory.ini',
                    colorized: true
                )
            }
        }
        */

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
//}