pipeline {
    agent { label 'master' } 
    stages {
        stage('Select Runner and Run Command') {
            steps {
                script {
                    def options = ['linux', 'python', 'ansible']
                    def userChoice = input(
                        id: 'userInput', 
                        message: 'Select a Runner to execute:',
                        parameters: [
                            [$class: 'ChoiceParameterDefinition', 
                             name: 'Runner', 
                             choices: options.join('\n'), 
                             description: 'Choose the type of runner you want to use']
                        ]
                    )
                    echo "You have selected: ${userChoice}"
                    sshagent(credentials: ['vagrant-key']) {
                        try {    
                            if (userChoice == 'linux') {
                                sh '/home/jenkins/check_server.sh' 
                                sh 'cat ${WORKSPACE}/jenkins_server_check.log'
                                archiveArtifacts artifacts: 'jenkins_server_check.log', allowEmptyArchive: true
                                sh 'rm -f ${WORKSPACE}/jenkins_server_check.log'
                            } else if (userChoice == 'python') {
                                sh 'echo "Running Python script..."'
                                sh "python3 /home/jenkins/check_server.py"
                                archiveArtifacts artifacts: 'jenkins_server_check.log', allowEmptyArchive: true
                                sh 'rm -f ${WORKSPACE}/jenkins_server_check.log'
                            } else if (userChoice == 'ansible') {
                                sh 'echo "Running Ansible script..."'
                                ansiblePlaybook disableHostKeyChecking: true, installation: 'ansible', inventory: "${INVENTORY}", playbook: "${ANSIBLE_PLAYBOOK}", vaultTmpPath: '' 
                            }
                        }catch (Exception e) {
                                echo "remote_control.sh failed, but continuing: ${e}"
                        }
                    }
                }
            }
        }
    }
}
