pipeline {
    stages {
        stage('Build') {
            steps {
                script {
                    echo "빌드 작업을 대기 중입니다..."
                    // GitHub 프라이빗 레포지토리에서 최신 태그 가져오기
                    def version = sh(script: 'git ls-remote --tags https://github.com/sesac-awscloud2-final-project-team2/test-aws-cicd.git | awk -F/ \'{print $3}\' | sort -V | tail -n1', returnStdout: true).trim()
                    def newVersion
                    
                    if (version) {
                        newVersion = version.tokenize('.').collect { it.toInteger() }
                        newVersion[-1] += 1
                        newVersion = newVersion.join('.')
                    } else {
                        newVersion = '0.1'
                    }
                    
                    echo "Docker 이미지 빌드 중: collector/dev01:${newVersion}"
                    sh "docker image build --platform linux/amd64 -t collector/dev01:${newVersion} ."
                    sh "docker tag collector/dev01:${newVersion} 257394490626.dkr.ecr.ap-northeast-2.amazonaws.com/collector/dev01:${newVersion}"
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    echo "ECR에 푸시 중: collector/dev01:${newVersion}"
                    sh "docker push 257394490626.dkr.ecr.ap-northeast-2.amazonaws.com/collector/dev01:${newVersion}"
                }
            }
        }
    }
}
