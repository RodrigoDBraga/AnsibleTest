pipeline {
    agent any
    // note that running this will also run
    // 'rm -rf '/home/jenkins/iProlepsisMonitoring''
    // "rm -rf "tmp/.git"
    // so be sure to verify that there's nothing important there before running this jenkinsfile
    parameters {
        string(name: 'REMOTE_DIR', defaultValue: '/home/jenkins/iProlepsisMonitoring', description: 'Remote directory for deployment')

    }
    
    environment {
        INVENTORY_FILE = "${WORKSPACE}/playbooks/inventory.ini"
        GIT_REPO = 'https://github.com/RodrigoDBraga/AnsibleTest'
        GIT_BRANCH = 'main'
        //
        MONITORING_SERVER_IP = '209.97.142.146'
        //
    }
    
    triggers {
        cron('0 0 1 */3 *') // cron('* * * * *') // Run every minute for testing purposes
    }


    stages {   
        
        stage('Determine Execution Type') {
            steps {
                script {
                    env.IS_SCHEDULED_RUN = currentBuild.getBuildCauses('hudson.triggers.TimerTrigger$TimerTriggerCause').size() > 0
                }
            }
        }

        stage('Checkout') {
            steps {
                git branch: env.GIT_BRANCH, url: env.GIT_REPO
            }
        }
        
        stage('Get IP Addresses and Create Inventory') {
            when {
                expression { !env.IS_SCHEDULED_RUN.toBoolean() }
            }
            steps {
                script {
                    createInventory()
                }
            }
        }
        
        stage('Run Ansible Playbook') {
            when {
                expression { !env.IS_SCHEDULED_RUN.toBoolean() }
            }
            steps {
                script {
                    def runningNodes = getRunningNodesFromInventory()
                    echo "Running Nodes (from inventory): ${runningNodes}"
                    
                    runningNodes.each { node ->
                        if (node.ip == env.MONITORING_SERVER_IP) {
                            runAnsibleOnMonitoringServer(node)
                        } else {
                            echo "is going through client servers"
                            runAnsibleOnClientServer(node)
                        }
                    }
                    echo "went through running nodes"
                }
            }
        }

        stage('Generate Report') {
            when {
                expression { env.IS_SCHEDULED_RUN.toBoolean() }
            }
            steps {
                script {
                    // Run the report generation script on the monitoring server
                    sh """
                        ssh root@${env.MONITORING_SERVER_IP} 'cd /home/jenkins/iProlepsisMonitoring && python3 generate_report.py'
                    """
                }
            }
        }
    }
    
    post {
    always {
        archiveArtifacts artifacts: 'playbooks/inventory.ini', fingerprint: true
        }
    }
}

def createInventory() {
    def nodeIpMap = [:]
    
    writeFile file: env.INVENTORY_FILE, text: "[Monitoring]\n"
    
    jenkins.model.Jenkins.instance.computers.each { computer ->
        def nodeName = computer.name
        
        if (nodeName && nodeName != "master" && computer.online) {
            def ipAddresses = computer.getChannel()?.call(new hudson.model.Computer.ListPossibleNames())
            if (ipAddresses) {
                def lastIP = ipAddresses.last()
                nodeIpMap[nodeName] = lastIP
                echo "Node: ${nodeName}, Last IP: ${lastIP}"
                sh "echo '${lastIP} ansible_host=${nodeName}' >> ${env.INVENTORY_FILE}"
            } else {
                echo "No IP addresses found for node: ${nodeName}"
            }
        }
    }
    
    echo "Discovered Running Nodes: ${nodeIpMap}"
    env.NODE_IP_MAP = nodeIpMap.collect { k, v -> "$k=$v" }.join(',')
}

def getRunningNodesFromInventory() {
    def runningNodes = []
    def inventory = readFile(env.INVENTORY_FILE)
    
    inventory.split('\n').each { line ->
        if (line && !line.startsWith('[')) {
            def (ip, hostPart) = line.tokenize() 
            def hostname = hostPart.split('=')[1]
            runningNodes.add([hostname: hostname, ip: ip])
        }
    }
    
    return runningNodes
}

def runAnsibleOnClientServer(node) {
    echo "got into the runansibleclientserver"
    sshagent([node.hostname]) {
        try {
            echo "went past the sshagent"
            sh "ssh -o StrictHostKeyChecking=no root@${node.ip} 'rm -rf ${params.REMOTE_DIR}'"
            sh """
                if [ -d "tmp/.git" ]; then
                    rm -rf "tmp/.git"
                fi
                mv ${WORKSPACE}/.git /tmp/.git
                scp -o StrictHostKeyChecking=no -r ${WORKSPACE} root@${node.ip}:${params.REMOTE_DIR}  
                mv /tmp/.git ${WORKSPACE}/

                # Install Ansible on the remote machine
                ssh -o StrictHostKeyChecking=no root@${node.ip} '
                    if ! command -v ansible-playbook &> /dev/null; then
                        apt update
                        apt install -y software-properties-common
                        apt-add-repository --yes --update ppa:ansible/ansible
                        apt install -y ansible
                    fi
                '

                ssh -o StrictHostKeyChecking=no root@${node.ip} 'ansible-playbook ${params.REMOTE_DIR}/playbooks/playbook.yml -i "localhost," -e "server_ip=${node.ip} remote_dir=${params.REMOTE_DIR} is_monitoring_server=false" -vvv'
            """
        } catch (Exception e) {
            echo "Error occurred while processing client server ${node.hostname}: ${e.message}"
        }
    }
}

def runAnsibleOnMonitoringServer(node) {
    
    sshagent([node.hostname]) {
        try {
            sh "ssh -o StrictHostKeyChecking=no root@${node.ip} 'rm -rf ${params.REMOTE_DIR}'"
            sh """
                if [ -d "tmp/.git" ]; then
                    rm -rf "tmp/.git"
                fi
                mv ${WORKSPACE}/.git /tmp/.git
                scp -o StrictHostKeyChecking=no -r ${WORKSPACE} root@${node.ip}:${params.REMOTE_DIR}  
                mv /tmp/.git ${WORKSPACE}/

                # Install Ansible on the remote machine
                ssh -o StrictHostKeyChecking=no root@${node.ip} '
                    if ! command -v ansible-playbook &> /dev/null; then
                        apt update
                        apt install -y software-properties-common
                        apt-add-repository --yes --update ppa:ansible/ansible
                        apt install -y ansible
                    fi
                '

                ssh -o StrictHostKeyChecking=no root@${node.ip} 'ansible-playbook ${params.REMOTE_DIR}/playbooks/playbook.yml -i "localhost," -e "server_ip=${node.ip} remote_dir=${params.REMOTE_DIR} is_monitoring_server=true" -vvv'
            """
        } catch (Exception e) {
            echo "Error occurred while processing monitoring server ${node.hostname}: ${e.message}"
        }
    }
}

/*
//think this is deprecated
def runAnsibleOnNodes(runningNodes) {
    runningNodes.each { node ->
        sshagent([node.hostname]) {
            try {
                sh "ssh -o StrictHostKeyChecking=no root@${node.ip} 'rm -rf ${params.REMOTE_DIR}'"
                sh """
                    if [ -d "tmp/.git" ]; then
                        rm -rf "tmp/.git"
                    fi
                    mv ${WORKSPACE}/.git /tmp/.git
                    scp -o StrictHostKeyChecking=no -r ${WORKSPACE} root@${node.ip}:${params.REMOTE_DIR}  
                    mv /tmp/.git ${WORKSPACE}/

                    # Install Ansible on the remote machine
                    ssh -o StrictHostKeyChecking=no root@${node.ip} '
                        if ! command -v ansible-playbook &> /dev/null; then
                            apt update
                            apt install -y software-properties-common
                            apt-add-repository --yes --update ppa:ansible/ansible
                            apt install -y ansible
                        fi
                    '

                    ssh -o StrictHostKeyChecking=no root@${node.ip} 'ansible-playbook ${params.REMOTE_DIR}/playbooks/playbook.yml -i "localhost," -e "server_ip=${node.ip} remote_dir=${params.REMOTE_DIR}" -vvv'
                """
            } catch (Exception e) {
                echo "Error occurred while processing node ${node.hostname}: ${e.message}"
                // Optionally, you can throw the error to fail the build
                // throw e
            }
        }
    }
}*/