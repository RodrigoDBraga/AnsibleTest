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
                    
                    // Use Jenkins API to get nodes safely
                    jenkins.model.Jenkins.instance.computers.each { computer ->
                        def nodeName = computer.name ?: 'master'
                        
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
                    
                    // Echo discovered running nodes
                    echo "Discovered Running Nodes: ${nodeIpMap}"
                    
                    // Store the map as a string representation
                    env.NODE_IP_MAP = nodeIpMap.collect { k, v -> "$k=$v" }.join(',')
                }
            }
        }
        /*
        stage('Discover Running Nodes') {
            steps {
                script {
                    workspacePath = env.WORKSPACE
                    INVENTORY_FILE = "${workspacePath}/playbooks/inventory.ini"

                    // Use a Map to store hostnames and IPs
                    def runningNodes = [:] 

                    // Collect Node Information
                    for (node in jenkins.model.Jenkins.instance.nodes) {
                        def computer = node.toComputer()
                        if (computer != null && computer.isOnline()) {
                        def nodeName = node.getNodeName()
                        def ip = computer.hostName
                        //def ip = computer.hostName
                        //def ip = sh(script: 'ip addr show eth0 | grep "inet " | awk \'{print $2}\' | cut -d/ -f1', returnStdout: true).trim() 
                        runningNodes[nodeName] = '64.226.69.178' //ip // Store both hostname and IP
                        def ip = '64.226.69.178'
                        echo "Running Nodes: ${runningNodes}"
                        
                        echo "Running Node: ${nodeName} with IP: ${ip}"
                        }
                    }

                    // Write to Inventory File (optional, if you still need it)
                    writeFile file: INVENTORY_FILE, text: "[Monitoring]\n"
                    runningNodes.each { hostname, ip ->
                        //writeFile file: INVENTORY_FILE, text: "${ip} ansible_host=${hostname}\n", append: true 
                        sh "echo '${ip} ansible_host=${hostname}' >> ${INVENTORY_FILE}" 
                    }

                    
                    echo "Discovered Running Nodes: ${runningNodes}"
                    //env.runningNodes = runningNodes.collect { hostname, ip -> [hostname: hostname, ip: ip] } 
                    }
      }
    }*/

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
