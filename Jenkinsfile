//import hudson.model.Computer
//import hudson.remoting.Callable
//import hudson.remoting.Future
//import org.jenkinsci.remoting.RoleChecker

pipeline {
    agent any

    /*
    environment {
        //SERVER_IP = ''
        SERVER_NAME = 'friendly_server_name' // Adjust as necessary
    }*/
    //environment {
        // Set this to 'true' for testing (create a container)
        // Set this to 'false' in client environments (discover existing containers)
        //CREATE_TEST_CONTAINER = 'true' 
        
        //++++workspacePath = env.WORKSPACE
        
        //++++INVENTORY_FILE = "${workspacePath}/playbooks/inventory.ini"
        // Optional: Filter for client containers (adjust based on naming conventions)
        //CLIENT_CONTAINER_FILTER = 'name=client-' 
    //}

    stages {   
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/RodrigoDBraga/AnsibleTest'
            }
        }
        /*
        stage('Get Node Information') {
            steps {
                script {
                    def onlineNodes = [:]
                    echo "got inside node information"
                    // 1. Get Online Nodes
                    def response = httpRequest(
                        url: "${env.JENKINS_URL}/computer/api/json",
                        httpMode: 'GET',
                        authentication: 'jenkins-user' // Replace with your credentials ID
                    )

                    def computers = jsonParse(response.content).computer

                    for (computer in computers) {
                        if (!computer.offline) {
                            def nodeName = computer.displayName

                            // 2. Get Possible IPs/Hostnames for Online Nodes
                            try {
                                def possibleNamesFuture = Computer.threadPoolForRemoting.submit(new Callable<List<String>, Exception>() {
                                    @Override
                                    List<String> call() throws Exception {
                                        def channel = Jenkins.instance.getNode(nodeName).computer.getChannel()
                                        if (channel != null) {
                                            return channel.call(new Computer.ListPossibleNames())
                                        } else {
                                            return []
                                        }
                                    }
                                })

                                def possibleNames = possibleNamesFuture.get() // Get the result
                                onlineNodes[nodeName] = possibleNames 
                            } catch (Exception ex) {
                                echo "Error getting possible names for ${nodeName}: ${ex.message}"
                                onlineNodes[nodeName] = ["Error retrieving IPs"] // Store an error message
                            }
                        } 
                    }

                    // 3. Output Results
                    onlineNodes.each { nodeName, ips ->
                        echo "Node: ${nodeName}, Possible IPs/Hostnames: ${ips}"
                    }
                }
            }
        }
        */
        stage('Discover Running Nodes') {
            steps {
                script {
                    workspacePath = env.WORKSPACE
                    INVENTORY_FILE = "${workspacePath}/playbooks/inventory.ini"
                    // Initialize inventory file
                    sh "echo '[Monitoring]' > ${INVENTORY_FILE}"
                    sh "echo '1'"
                    sh "echo ${INVENTORY_FILE}"
                    sh "whoami"
                    // Get all nodes and their IPs
                    def nodes = jenkins.model.Jenkins.instance.nodes
                    def runningNodes = []

                    for (node in nodes) {
                        def computer = node.toComputer()
                        if (computer != null && computer.isOnline()) {
                            def nodeName = node.getNodeName()
                            def ip = computer.hostName
                            runningNodes.add(ip)
                            echo "Running Node: ${nodeName} with IP: ${ip}"
                        }
                    }
                    nodes = 0
                    echo "${runningNodes}"
                    // Write IPs to the inventory file
                    for (ip in runningNodes) {
                        sh "echo '${ip}' >> ${INVENTORY_FILE}"
                    }

                    sh "echo '6'"

                    // Print the discovered nodes
                    echo "Discovered Running Nodes: ${runningNodes.join(', ')}"

                    /*
                    // Initialize inventory file
                    sh "echo '[Monitoring]' > ${INVENTORY_FILE}"
                    // Get all nodes
                    def nodes = jenkins.model.Jenkins.instance.nodes
                    def runningNodes = []
                    // Iterate over each node
                    for (node in nodes) {
                        def computer = node.toComputer()
                        if (computer != null && computer.isOnline()) {
                            // Get node name and IP address
                            def nodeName = node.getNodeName()
                            def ip = computer.hostName
                            //runningNodes.add([name: nodeName, ip: ip])
                            runningNodes.add(ip)
                            echo "Running Node: ${nodeName} with IP: ${ip}"
                            // Append to inventory file
                            echo "${ip} >> ${INVENTORY_FILE}"  
                        }
                    }
                    // Print the discovered nodes
                    sh "echo ${ip} >> ${INVENTORY_FILE}"
                    echo "Discovered Running Nodes: ${runningNodes}"
                    */
                }
            }
        }


        /*
        stage('Update Inventory') {
            steps {
                script {
                    workspacePath = env.WORKSPACE
        
                    INVENTORY_FILE = "${workspacePath}/playbooks/inventory.ini"
                    sh "echo '${INVENTORY_FILE}'"
                    // Clear the existing content in the inventory file
                    sh "echo '[Monitoring]' > ${INVENTORY_FILE}"
                    sh "echo 'outside of the first echo'"
                    // Discover IPs of all nodes labeled with 'vm'
                    def vmNodes = jenkins.model.Jenkins.instance.nodes.findAll { node ->
                        node.getLabelString().contains('vm')
                    }
                    sh "echo ${vmNodes}"
                    vmNodes.each { node ->
                        def computer = node.toComputer()
                        
                        if (computer.isOnline()) { // Check if the node is online
                            def ip = computer.getHostName()
                            echo "IP for ${node.getDisplayName()}: ${ip}"
                            sh "echo ${ip} >> ${INVENTORY_FILE}"
                        } else {
                            echo "Node ${node.getDisplayName()} is offline."
                        }
                        
                        //def ip = computer.getHostName()
                        //echo "IP for ${node.getDisplayName()}: ${ip}"
                        // Append IP to the inventory file
                        //sh "echo ${ip} >> ${INVENTORY_FILE}"
                        //sh "this is the ip: ${ip}"
                        //exit
                        
                    }
                }
            }
        }
        */

        /*
        stage('Deploy monitoring') {
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
                        
                    }
                }        }
        }
        */

        stage('Run Ansible Playbook') {
            steps {
                script {
                    workspacePath = env.WORKSPACE
        
                    INVENTORY_FILE = "${workspacePath}/playbooks/inventory.ini"

                    def inventory = readFile("${INVENTORY_FILE}")
                    echo "Inventory File:\n${inventory}"
                    
                    //def runningNodes = inventory.split('\n').findAll { it }
                    def runningNodes = inventory.split('\n').findAll { it && !it.startsWith('[') }
                    runningNodes.each { ip ->
                        sshagent(['vm1']) {
                            sh """
                                ssh-agent sh -c '
                                ssh-add ${SSH_KEY};
                                scp -o StrictHostKeyChecking=no -r ${workspacePath} jenkins@${ip}:/home/jenkins/iProlepsisMonitoring;
                                ssh -o StrictHostKeyChecking=no jenkins@${ip} \
                                'ansible-playbook home/jenkins/iProlepsisMonitoring/playbooks/playbook.yml -i home/jenkins/iProlepsisMonitoring/playbooks/inventory.ini'
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


        stage('Run Ansible Playbook - old') {
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
