pipeline {
    agent any
    stages {   
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/RodrigoDBraga/AnsibleTest'
            }
        }

        stage('Discover Running Nodes') {
            steps {
                script {
                    workspacePath = env.WORKSPACE
                    INVENTORY_FILE = "${workspacePath}/playbooks/inventory.ini"

                    def runningNodes = [:]

                    // Collect Node Information
                    for (node in jenkins.model.Jenkins.instance.nodes) {
                        def computer = node.toComputer()
                        if (computer != null && computer.isOnline()) {
                            def nodeName = node.getNodeName()
                            def dockerIP = computer.hostName

                            // Execute a command on the node to get the actual IP address
                            node(nodeName) {
                                def actualIP = sh(script: "hostname -I | awk '{print \$1}'", returnStdout: true).trim()
                                runningNodes[nodeName] = actualIP
                                echo "Running Node: ${nodeName} with IP: ${actualIP}"
                            }
                        }
                    }

                    // Write to Inventory File (optional, if you still need it)
                    writeFile file: INVENTORY_FILE, text: "[Monitoring]\n"
                    runningNodes.each { hostname, ip ->
                        sh "echo '${ip} ansible_host=${hostname}' >> ${INVENTORY_FILE}"
                    }

                    echo "Discovered Running Nodes: ${runningNodes}"
                }
            }
        }  
       //sort of requires a check for packages in the vms at some stage due to ansible and so on, but....       
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
                        runningNodes[nodeName] = ip // Store both hostname and IP
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
        /*
        stage('Get Connected Node SSH Info') {
            steps {
                script {
                    def jenkins = Jenkins.getInstance()
                    def computerSet = jenkins.getComputers()

                    for (computer in computerSet) {
                        if (computer instanceof SlaveComputer && computer.isOnline()) { // Only connected slaves
                            def slaveComputer = computer as SlaveComputer
                            def channel = slaveComputer.getChannel()
                            if (channel != null) {
                                def remoteAddress = channel.getRemoteAddress()
                                def host = remoteAddress.getHostName()
                                def ip = InetAddress.getByName(host).getHostAddress() // Resolve hostname to IP

                                echo "Node: ${computer.getName()}, Host: ${host}, SSH IP: ${ip}"
                            } 
                        } 
                    }
                }
            }*/

        stage('Run Ansible Playbook') {
            steps {
                script {
                    workspacePath = env.WORKSPACE
                    INVENTORY_FILE = "${workspacePath}/playbooks/inventory.ini"
                    //echo "correctly started run ansible playbook"

                    def runningNodes = []
                    def inventory = readFile("${INVENTORY_FILE}")

                    inventory.split('\n').each { line ->
                        if (line && !line.startsWith('[')) {
                            def (ip, hostPart) = line.tokenize() // Split by space
                            def hostname = hostPart.split('=')[1] // Extract hostname
                            runningNodes.add([hostname: hostname, ip: ip])
                        }
                    }

                    echo "Running Nodes (from inventory): ${runningNodes}"

                    runningNodes.each { node ->
                        sshagent([node.hostname]) {
                            //sh "ssh-keyscan -H ${node.ip} >> /var/jenkins_home/.ssh/known_hosts" 
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
