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
                                sh 'echo "Running Linux script..."'
                                sh "/home/jenkins/remote_control.sh ${params.INVENTORY} ${params.COMMAND}" 
                                archiveArtifacts artifacts: "remote_control_${BUILD_NUMBER}.log", allowEmptyArchive: true
                                sh "rm -f ${WORKSPACE}/remote_control_${BUILD_NUMBER}.log"
                            } else if (userChoice == 'python') {
                                sh 'echo "Running Python script..."'
                                sh "python3 /home/jenkins/remote_control.py ${params.INVENTORY} ${params.COMMAND}"
                                archiveArtifacts artifacts: "remote_control_${BUILD_NUMBER}.log", allowEmptyArchive: true
                                sh "rm -f ${WORKSPACE}/remote_control_${BUILD_NUMBER}.log"
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
