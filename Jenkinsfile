// Start Generation Here
pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // 현재 작업공간을 복사하여 도커 이미지를 빌드
                    echo '도커 이미지 빌드를 시작합니다.' // 로그 추가
                    sh 'docker image build --platform linux/amd64 -t collector/dev01 .'
                    echo '도커 이미지 빌드가 완료되었습니다.' // 로그 추가
                }
            }
        }
        stage('Tag Docker Image') {
            steps {
                script {
                    // ECR에 업로드할 태그 추가
                    echo '도커 이미지에 태그를 추가합니다.' // 로그 추가
                    sh 'docker tag collector/dev01:latest 257394490626.dkr.ecr.ap-northeast-2.amazonaws.com/collector/dev01:latest'
                    echo '도커 이미지 태그 추가가 완료되었습니다.' // 로그 추가
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    // ECR에 도커 이미지 업로드
                    echo 'ECR에 도커 이미지를 업로드합니다.' // 로그 추가
                    sh 'docker push 257394490626.dkr.ecr.ap-northeast-2.amazonaws.com/collector/dev01:latest'
                    echo 'ECR에 도커 이미지 업로드가 완료되었습니다.' // 로그 추가
                }
            }
        }
    }
}
