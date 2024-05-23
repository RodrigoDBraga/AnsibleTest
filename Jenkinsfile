pipeline {
    agent any
    parameters {
        string(name: 'SERVER_NAME', defaultValue: 'Server_Portugal', description: 'Friendly name of the server')
        string(name: 'SERVER_IP', defaultValue: '192.168.1.19', description: 'IP address of the server')
    }
    stages {
        /*
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
        */
        
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
                    def ip_address = sh(script: "hostname -I | awk '{print \$1}'", returnStdout: true).trim() // this is currently getting the docker/jenkins ip and not the machine itself
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
                echo "ansibleplaybook"//"Fetched IP: ${env.SERVER_IP}"
                /*
                ansiblePlaybook(
                    playbook: 'playbooks/playbook.yml',
                    inventory: 'playbooks/inventory.ini',
                    extras: '--extra-vars "server_name=${env.SERVER_NAME} server_ip=${env.SERVER_IP}"'
                    //extras: '--extra-vars "server_ip=${env.SERVER_IP}"'
                )
                sh 'find /usr -name ansible -type d'
                sh 'find /var/jenkins_home/plugins -name ansible -type f'
                sh 'sudo find / -name ansible -type f'
                sh 'sudo find / -name ansible -type d'
                println "Ansible installation directory: ${ansible.home}"
                sh 'ansible --version'
                sh 'which ansible-playbook'
                */
                sh 'echo $PATH'
                sh 'pwd && ls -ltr'
                echo "1"
                sh 'find $JENKINS_HOME -name ansible -type d'               
                echo "2"
                /*
                // this tells you what version of ansible you have and that it is actually installed in the server
                script {
                    def installedPlugins = Jenkins.instance.pluginManager.plugins
                    for (plugin in installedPlugins) {
                        echo "Plugin Name: ${plugin.getShortName()}, Version: ${plugin.getVersion()}"
                        if (plugin.getShortName() == 'ansible') {
                            echo "Found Ansible plugin. Exiting loop."
                            break
                        }
                }
                }*/
                //sh 'find $JENKINS_HOME -name ansiblePlaybook'
                //sh 'ansible --version'
                echo "3"
                
                ansiblePlaybook(
                            playbook: 'playbooks/playbook.yml',
                            inventory: 'playbooks/inventory.ini',//,
                            extras: '--extra-vars "server_ip=${env.SERVER_IP}"' // can also put here the server_name depending on what we are doing
                )
                
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