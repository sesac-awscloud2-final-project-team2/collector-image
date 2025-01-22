pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = "257394490626"
        AWS_DEFAULT_REGION = "ap-northeast-2"
        IMAGE_REPO_NAME = "collector/dev01"
        IMAGE_TAG = "latest"
        REPOSITORY_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}"
        CREDENTIAL_ID = 'AKIATX3PIHUBGGKLQA2F'
        ACCESS_KEY_VARIABLE = 'dynamodb'
        SECRET_ACCESS_KEY = '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'
    }
    stages {
        stage('ECR Login') {
            steps {
                script {
                    withCredentials([aws(credentialsId: "${CREDENTIAL_ID}", accessKeyVariable: "${ACCESS_KEY_VARIABLE}", secretKeyVariable: "${SECRET_ACCESS_KEY}")]) {
                        sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo '도커 이미지 빌드를 시작합니다.'
                    sh "docker image build --platform linux/amd64 -t ${IMAGE_REPO_NAME}:${IMAGE_TAG} ."
                    echo '도커 이미지 빌드가 완료되었습니다.'
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                script {
                    echo '도커 이미지에 태그를 추가합니다.'
                    sh "docker tag ${IMAGE_REPO_NAME}:${IMAGE_TAG} ${REPOSITORY_URI}:${IMAGE_TAG}"
                    echo '도커 이미지 태그 추가가 완료되었습니다.'
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    echo 'ECR에 도커 이미지를 업로드합니다.'
                    sh "docker push ${REPOSITORY_URI}:${IMAGE_TAG}"
                    echo 'ECR에 도커 이미지 업로드가 완료되었습니다.'
                }
            }
        }
    }
}
