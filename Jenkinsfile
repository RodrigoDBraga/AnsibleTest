pipeline {
    agent any
    stages {   
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/RodrigoDBraga/AnsibleTest'
            }
        }
       //sort of requires a check for packages in the vms at some stage due to ansible and so on, but....       
        stage('Get IP Addresses and Create Inventory') {
            steps {
                script {
                    def nodeIpMap = [:]
                    
                    // Define the inventory file path
                    def workspacePath = env.WORKSPACE
                    def INVENTORY_FILE = "${workspacePath}/playbooks/inventory.ini"
                    
                    // Create the inventory file with the header
                    writeFile file: INVENTORY_FILE, text: "[Monitoring]\n"
                    
                    // Use Jenkins API to get nodes safely, excluding the master
                    jenkins.model.Jenkins.instance.computers.each { computer ->
                        def nodeName = computer.name
                        
                        // Skip the master node
                        if (nodeName && nodeName != "master") {
                            if (computer.online) {
                                def ipAddresses = computer.getChannel()?.call(new hudson.model.Computer.ListPossibleNames())
                                if (ipAddresses) {
                                    def lastIP = ipAddresses.last()
                                    nodeIpMap[nodeName] = lastIP
                                    echo "Node: ${nodeName}, Last IP: ${lastIP}"
                                    
                                    // Append to the inventory file
                                    sh "echo '${lastIP} ansible_host=${nodeName}' >> ${INVENTORY_FILE}"
                                } else {
                                    echo "No IP addresses found for node: ${nodeName}"
                                }
                            } else {
                                echo "Node '${nodeName}' is offline or not accessible"
                            }
                        }
                    }
                    
                    // Echo discovered running nodes
                    echo "Discovered Running Nodes: ${nodeIpMap}"
                    
                    // Store the map as a string representation
                    env.NODE_IP_MAP = nodeIpMap.collect { k, v -> "$k=$v" }.join(',')
                }
            }
        }
        

        stage('Run Ansible Playbook') {
            steps {
                script {
                    workspacePath = env.WORKSPACE
                    INVENTORY_FILE = "${workspacePath}/playbooks/inventory.ini"
                    def runningNodes = []
                    def inventory = readFile("${INVENTORY_FILE}")

                    inventory.split('\n').each { line ->
                        if (line && !line.startsWith('[')) {
                            def (ip, hostPart) = line.tokenize() 
                            def hostname = hostPart.split('=')[1]
                            runningNodes.add([hostname: hostname, ip: ip])
                        }
                    }

                    echo "Running Nodes (from inventory): ${runningNodes}"

                    runningNodes.each { node ->
                        sshagent([node.hostname]) {
                            sh "ssh -o StrictHostKeyChecking=no root@${node.ip} 'rm -rf /home/jenkins/iProlepsisMonitoring'"
                            sh """
                                if [ -d "tmp/.git" ]; then
                                    rm -rf "tmp/.git"
                                fi
                                mv ${workspacePath}/.git /tmp/.git
                                scp -o StrictHostKeyChecking=no -r ${workspacePath} root@${node.ip}:/home/jenkins/iProlepsisMonitoring  
                                mv /tmp/.git ${workspacePath}/
                                ssh -o StrictHostKeyChecking=no root@${node.ip} 'ansible-playbook /home/jenkins/iProlepsisMonitoring/playbooks/playbook.yml -i "localhost," -e server_ip=${node.ip} -vvv'
                            """
                        }
                    }
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
        
      


    }
        
}
