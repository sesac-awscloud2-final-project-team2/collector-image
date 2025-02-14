'''
데이터를 테이블에 저장
'''
import boto3
from ctl_logger import CustomLogger
logger = CustomLogger("Collector")

region_name = "ap-northeast-2"

# DynamoDB 클라이언트 생성
dynamodb_client = boto3.client(
    'dynamodb',
    region_name=region_name
)

class ValidData:
    def __init__(self, data: dict, table_name: str) -> None:
        self.data = data
        self.table_name = table_name

    def __call__(self) -> dict:
        if self.table_name == "user":
            result = {
                'user_id': {'S': self.data['user_id']},
                'username': {'S': self.data['username']},
                'email': {'S': self.data['email']},
                'password_hash': {'S': self.data['password_hash']},
                'name': {'S': self.data['name']},
                'gender': {'S': self.data['gender']},
                'birth_date': {'S': self.data['birth_date']},
                'nationality': {'S': self.data['nationality']},
                'profile_image_url': {'S': self.data['profile_image_url']},
                'preferred_language': {'S': self.data['preferred_language']},
                'phone_number': {'S': self.data['phone_number']},
                'is_verified': {'BOOL': self.data['is_verified']},
                'created_at': {'S': self.data['created_at']},
                'status': {'S': self.data['status']}
            }
        elif self.table_name == "trip":
            result = {
                'trip_id': {'S': self.data['trip_id']},
                'user_id': {'S': self.data['user_id']},
                'title': {'S': self.data['title']},
                'start_date': {'S': self.data['start_date']},
                'end_date': {'S': self.data['end_date']},
                'description': {'S': self.data['description']},
                'country': {'S': self.data['country']},
                'region': {'S': self.data['region']},
                'travel_type': {'S': self.data['travel_type']},
                'budget': {'N': str(self.data['budget'])},
                'transportation_type': {'S': self.data['transportation_type']},
                'status': {'S': self.data['status']},
                'privacy_level': {'S': self.data['privacy_level']},
                'created_at': {'S': self.data['created_at']}
            }
        elif self.table_name == "experience":
            result = {
                'experience_id': {'S': self.data['experience_id']},
                'user_id': {'S': self.data['user_id']},
                'trip_id': {'S': self.data['trip_id']},
                'experience_type': {'S': self.data['experience_type']},
                'experience_name': {'S': self.data['experience_name']},
                'rating': {'N': str(self.data['rating'])},
                'review': {'S': self.data['review']},
                'price': {'N': str(self.data['price'])},
                'currency': {'S': self.data['currency']},
                'experience_date': {'S': self.data['experience_date']},
                'details': {'S': str(self.data['details'])},
                'place': {
                    'M': {
                        'place_name': {'S': self.data['place']['place_name']},
                        'address': {'S': self.data['place']['address']},
                        'latitude': {'N': str(self.data['place']['latitude'])},
                        'longitude': {'N': str(self.data['place']['longitude'])},
                        'country': {'S': self.data['place']['country']},
                        'city': {'S': self.data['place']['city']},
                        'category': {'S': self.data['place']['category']},
                        'accessibility': {'S': self.data['place']['accessibility']}
                    }
                },
                'photo': {
                    'M': {
                        'file_name': {'S': self.data['photo']['file_name']},
                        'file_path': {'S': self.data['photo']['file_path']},
                        'file_size': {'N': str(self.data['photo']['file_size'])},
                        'file_type': {'S': self.data['photo']['file_type']},
                        'caption': {'S': self.data['photo']['caption']},
                        'photo_latitude': {'N': str(self.data['photo']['photo_latitude'])},
                        'photo_longitude': {'N': str(self.data['photo']['photo_longitude'])},
                        'taken_at': {'S': self.data['photo']['taken_at']},
                        'is_public': {'BOOL': self.data['photo']['is_public']}
                    }
                },
                'created_at': {'S': self.data['created_at']}
            }
        else:
            raise "Wrong Table Name"

        return result


def save_dynamodb_table(data:dict, table_name:str):
    """
    json string 형태의 data를 table_name을 이름으로 하는 테이블에 저장하는 함수
    """
    start_time = logger.start('save_dynamodb_table')
    try:
        valid_item = ValidData(data, table_name)
        
        response = dynamodb_client.put_item(
            TableName=table_name,
            Item=valid_item()
        )
        logger.dynamodb_operation('put_item', table_name, 1, start_time)
        logger.finish('save_dynamodb_table')
        return {
            "statusCode": 200,
            "message": "Data saved successfully",
            "response": response
        }
    except Exception as e:
        logger.error('Failed save_dynamo_table', e)
        return {
            "statusCode": 500,
            "message": "Error saving data",
            "error": str(e)
        }
    
if __name__ == "__main__":
    # 예시 데이터 생성
    example_data = {
        'user_id': 'test',
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
    
    save_dynamodb_table(example_data, "user")