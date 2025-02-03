# Collector
> 수신된 데이터를 dynamodb에 저장

## 이미지 ECR 업로드
`aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 390844761387.dkr.ecr.ap-northeast-2.amazonaws.com`
`docker image build --platform linux/amd64 -t collector .`
`docker tag collector:latest 390844761387.dkr.ecr.ap-northeast-2.amazonaws.com/collector:latest`
`docker push 390844761387.dkr.ecr.ap-northeast-2.amazonaws.com/collector:latest`