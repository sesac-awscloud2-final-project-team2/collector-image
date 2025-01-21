# Start Generation Here
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    def version = sh(script: 'git describe --tags --abbrev=0', returnStdout: true).trim()
                    def newVersion = version.tokenize('.').collect { it.toInteger() }
                    newVersion[-1] += 1
                    newVersion = newVersion.join('.')
                    
                    sh "docker image build --platform linux/amd64 -t collector/dev01:${newVersion} ."
                    sh "docker tag collector/dev01:${newVersion} 257394490626.dkr.ecr.ap-northeast-2.amazonaws.com/collector/dev01:${newVersion}"
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    sh "docker push 257394490626.dkr.ecr.ap-northeast-2.amazonaws.com/collector/dev01:${newVersion}"
                }
            }
        }
    }
}

