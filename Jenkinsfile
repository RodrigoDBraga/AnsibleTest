pipeline {
    agent any

    /*
    environment {
        //SERVER_IP = ''
        SERVER_NAME = 'friendly_server_name' // Adjust as necessary
    }*/
    environment {
        // Set this to 'true' for testing (create a container)
        // Set this to 'false' in client environments (discover existing containers)
        //CREATE_TEST_CONTAINER = 'true' 
        INVENTORY_FILE = "${workspacePath}/playbooks/inventory.ini"
        // Optional: Filter for client containers (adjust based on naming conventions)
        //CLIENT_CONTAINER_FILTER = 'name=client-' 
    }

    stages {   
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/RodrigoDBraga/AnsibleTest'
            }
        }

        stage('Update Inventory') {
            steps {
                script {
                    // Clear the existing content in the inventory file
                    sh "echo '[Monitoring]' > ${INVENTORY_FILE}"
                    
                    // Discover IPs of all nodes labeled with 'vm'
                    def vmNodes = jenkins.model.Jenkins.instance.nodes.findAll { node ->
                        node.getLabelString().contains('vm')
                    }
                    
                    vmNodes.each { node ->
                        def computer = node.toComputer()
                        def ip = computer.getHostName()
                        echo "IP for ${node.getDisplayName()}: ${ip}"
                        // Append IP to the inventory file
                        sh "echo ${ip} >> ${INVENTORY_FILE}"
                    }
                }
            }
        }
        


        stage('Deploy Monitoring') {
                steps {
                    script {
                        //def vms = ['vm1', 'vm2']
                        def vms = ['172.17.0.3']
                        
                        def workspacePath = env.WORKSPACE
                        
                        def vmNodes = jenkins.model.Jenkins.instance.nodes.findAll { node ->
                            node.getLabelString().contains('vm')
                        }
                        
                        vmNodes.each { node ->
                        def computer = node.toComputer()
                        def ip = computer.getHostName()
                        sshagent(['vm1']) {
                            sh """
                                ssh-agent sh -c '
                                ssh-add ${SSH_KEY};
                                scp -o StrictHostKeyChecking=no -r ${workspacePath} jenkins@${ip}:/home/jenkins/iProlepsisMonitoring;
                                ssh -o StrictHostKeyChecking=no jenkins@${ip} "ansible-playbook /home/jenkins/iProlepsisMonitoring/playbooks/playbook.yml -i /home/jenkins/iProlepsisMonitoring/playbooks/inventory.ini"';

                                #ssh -o StrictHostKeyChecking=no jenkins@${ip} \
                                #'ansible-playbook /home/jenkins/iProlepsisMonitoring/playbooks/playbook.yml \
                                #-i /home/jenkins/iProlepsisMonitoring/playbooks/inventory.ini'
                            """
                        }
                        /*
                        withCredentials([sshUserPrivateKey(credentialsId: 'vm1', keyFileVariable: 'SSH_KEY')]) {
                        for (vm in vms) {
                            sshagent(['vm1']) {
                            sh """
                                ssh-agent sh -c '
                                ssh-add ${SSH_KEY};
                                scp -o StrictHostKeyChecking=no -r ${workspacePath} jenkins@${vm}:/home/jenkins/iProlepsisMonitoring;
                                ssh -o StrictHostKeyChecking=no jenkins@${vm} "ansible-playbook /home/jenkins/iProlepsisMonitoring/playbooks/playbook.yml -i /home/jenkins/iProlepsisMonitoring/playbooks/inventory.ini"';

                                #ansible-playbook playbooks/playbook.yml -i playbooks/inventory.ini 
                                #scp -o StrictHostKeyChecking=no -r client/ jenkins@${vm}:/home/jenkins/;
                                #ansible-playbook playbooks/playbook.yml -i playbooks/inventory.ini 
                                #ssh -o StrictHostKeyChecking=no jenkins@${vm} "docker-compose -f /home/jenkins/client/docker-compose-client-monitor.yml up -d"
                                '
                            """}
                        }
                        }*/
                    }
                }
        }


        /* YOU DO NEED THIS ACTUALLY SO DON'T DELETE IT
        stage('Install Ansible') {
            steps {
                sh '''
                    sudo apt update
                    sudo apt install -y ansible
                '''
            }
        }*/
        
        /*
        stage('Container Setup') {
            steps {
                script {
                    if (env.CREATE_TEST_CONTAINER == 'true') {
                        // Create a test Ubuntu container
                        sh """
                            docker run -d -it --name ubuntu-test-container \
                                -v /var/run/docker.sock:/var/run/docker.sock \
                                ubuntu:latest /bin/bash
                        """
                        // Get the IP of the newly created container
                        env.TARGET_CONTAINER_IP = sh(returnStdout: true, script: "docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ubuntu-test-container").trim()
                    } else {
                        // Discover existing client container IPs
                        def clientContainerIPs = sh(returnStdout: true, script: """
                            docker ps -aq --filter "${env.CLIENT_CONTAINER_FILTER}" | xargs -I {} docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' {}
                        """).trim().split("\n").findAll { it.trim() != "" }

                        if (clientContainerIPs.isEmpty()) {
                            error("No client containers found with filter: ${env.CLIENT_CONTAINER_FILTER}")
                        } else {
                            env.TARGET_CONTAINER_IP = clientContainerIPs[0] // Use the first IP found
                            echo "Discovered client container IPs: ${clientContainerIPs.join(', ')}"
                        }
                    }
                }
            }
        }*/
        
        /*
        stage('Update Ansible Inventory') {
            steps {
                script {
                    def containerIps = env.TARGET_CONTAINER_IPS.split('\n').collect { it.trim() }.findAll { it != "" }
                    def inventoryContent = "[Monitoring]\n"
                    for (ip in containerIps) {
                        inventoryContent += "${ip} ansible_user=${env.ANSIBLE_USER}\n"
                    }
                    writeFile file: 'ansible/inventory.ini', text: inventoryContent
                    sh "cat ansible/inventory.ini" // Optional: Print the inventory file
                }
            }
        }*/

        /*
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
                    writeFile file: 'ansible/inventory.ini', text: inventoryContent
                }
            }
        }*/


        stage('Run Ansible Playbook') {
            steps {
                    /*
                    sh '''
                        ansible-playbook -i playbooks/playbook.yml playbooks/inventory.ini 
                    '''
                    */
                    /*
                    //this is the current version i am running, the one above this doesn't work because the -i needs to be before the inventory and not the playbook
                    sh '''
                        ansible-playbook playbooks/playbook.yml -i playbooks/inventory.ini 
                    '''*/
                    //withCredentials([sshUserPrivateKey(credentialsId: 'vm1', keyFileVariable: 'SSH_KEY')])
                    /*
                    withCredentials([usernamePassword(credentialsId: 'ansible-credentials-id', usernameVariable: 'ANSIBLE_USER', passwordVariable: 'ANSIBLE_PASSWORD')]) {
                        sh '''
                            ansible-playbook -i playbooks/inventory.ini playbooks/playbook.yml
                        '''
                        */
                        echo "with steel and strength"
            
                
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
}