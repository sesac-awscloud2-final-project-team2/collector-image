'''
데이터를 테이블에 저장
'''

import boto3
from secret_manager import get_secret

secrets = get_secret()

collector_port = int(secrets.get("COLLECTOR_PORT", 30000)) # 기본값30000
aws_access_key_id = secrets['DYNAMO_ACCESS_KEY_ID']
aws_secret_access_key = secrets['DYNAMO_SECRET_ACCESS_KEY']
region_name = secrets['DYNAMO_REGION']

# DynamoDB 클라이언트 생성
dynamodb_client = boto3.client(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

def save_dynamodb_table(data:str, table_name:str):
    """
    json string 형태의 data를 table_name을 이름으로 하는 테이블에 저장하는 함수
    """
    try:
        response = dynamodb_client.put_item(
            TableName=table_name,
            Item={
                'user_id': {'S': data['user_id']},
                'username': {'S': data['username']},
                'email': {'S': data['email']},
                'password_hash': {'S': data['password_hash']},
                'name': {'S': data['name']},
                'gender': {'S': data['gender']},
                'birth_date': {'S': data['birth_date']},
                'nationality': {'S': data['nationality']},
                'profile_image_url': {'S': data['profile_image_url']},
                'preferred_language': {'S': data['preferred_language']},
                'phone_number': {'S': data['phone_number']},
                'is_verified': {'BOOL': data['is_verified']},
                'created_at': {'S': data['created_at']},
                'status': {'S': data['status']}
            }
        )
        return {
            "statusCode": 200,
            "message": "Data saved successfully",
            "response": response
        }
    except Exception as e:
        print(f"Error querying items: {e}")
        return {
            "statusCode": 500,
            "message": "Error saving data",
            "error": str(e)
        }
    
if __name__ == "__main__":
    # 예시 데이터 생성
    example_data = {
        'user_id': '12345',
        'username': 'test_user',
        'email': 'test@example.com',
        'password_hash': 'hashed_password',
        'name': '홍길동',
        'gender': '남성',
        'birth_date': '1990-01-01',
        'nationality': '대한민국',
        'profile_image_url': 'http://example.com/profile.jpg',
        'preferred_language': '한국어',
        'phone_number': '010-1234-5678',
        'is_verified': True,
        'created_at': '2023-01-01T00:00:00Z',
        'status': 'active'
    }
    
    save_dynamodb_table(example_data, "join")