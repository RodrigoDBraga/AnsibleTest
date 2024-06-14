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

                    // Print Discovered Nodes
                    echo "Discovered Running Nodes: ${runningNodes}"

                    // Store runningNodes in the global environment as a list of maps
                    env.runningNodes = runningNodes.collect { hostname, ip -> [hostname: hostname, ip: ip] } 
                    }
      }
    }

        stage('Run Ansible Playbook') {
            steps {
                script {
                    workspacePath = env.WORKSPACE
                    INVENTORY_FILE = "${workspacePath}/playbooks/inventory.ini"
                    echo "correctly started run ansible playbook"

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
                            sh "ssh -o StrictHostKeyChecking=no jenkins@${node.ip} 'rm -rf /home/jenkins/iProlepsisMonitoring'"
                            sh """
                                if [ -d "tmp/.git" ]; then
                                    rm -rf "tmp/.git"
                                fi
                                mv ${workspacePath}/.git /tmp/.git
                                scp -o StrictHostKeyChecking=no -r ${workspacePath} jenkins@${node.ip}:/home/jenkins/iProlepsisMonitoring  
                                mv /tmp/.git ${workspacePath}/
                                ssh -o StrictHostKeyChecking=no jenkins@${node.ip} 'ansible-playbook /home/jenkins/iProlepsisMonitoring/playbooks/playbook.yml -i "localhost," -e server_ip=${node.ip} -vvv'
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
                        echo "old ansible playbook test"
            
                
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
