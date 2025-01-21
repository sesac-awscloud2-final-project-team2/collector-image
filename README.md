# Collector
> 수신된 데이터를 dynamodb에 저장

## 이미지 ECR 업로드
`docker image build --platform linux/amd64 -t collector/dev01 .`
`docker tag collector/dev01:latest 257394490626.dkr.ecr.ap-northeast-2.amazonaws.com/collector/dev01:latest`
`docker push 257394490626.dkr.ecr.ap-northeast-2.amazonaws.com/collector/dev01:latest`