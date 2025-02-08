from flask import Flask, request, jsonify
from load_dynamodb import save_dynamodb_table
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/join', methods=['POST'])
def join():
    user_info = request.json
    
    # user_info를 데이터베이스에 저장
    try:
        dynamo_save_result = save_dynamodb_table(user_info, 'user')
        logging.info("사용자 등록 성공: %s", dynamo_save_result)
        return jsonify({"message": "User registered successfully", "user": dynamo_save_result}), 201
    
    except Exception as e:
        logging.error("사용자 등록 실패: %s", str(e))
        return jsonify({"message": "User registration failed", "error": str(e)}), 500

@app.route('/trip', methods=['POST'])
def trip():
    trip_info = request.json
    
    # trip_info 데이터베이스에 저장 (+유효성 검사)
    try:
        dynamo_save_result = save_dynamodb_table(trip_info, 'trip')
        logging.info("여행 데이터 저장 성공: %s", dynamo_save_result)
        return jsonify({"message": "Trip data save successfully", "user": dynamo_save_result}), 201
    
    except Exception as e:
        logging.error("여행 데이터 저장 실패: %s", str(e))
        return jsonify({"message": "Trip data save failed", "error": str(e)}), 500

@app.route('/experience', methods=['POST'])
def experience():
    experience_info = request.json
    
    # experience_info를 데이터베이스에 저장 (+유효성 검사)
    try:
        dynamo_save_result = save_dynamodb_table(experience_info, 'experience')
        logging.info("경험 데이터 저장 성공: %s", dynamo_save_result)
        return jsonify({"message": "Experience data save successfully", "user": dynamo_save_result}), 201
    
    except Exception as e:
        logging.error("경험 데이터 저장 실패: %s", str(e))
        return jsonify({"message": "Experience data save failed", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30001)
