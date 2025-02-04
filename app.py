from flask import Flask, request, jsonify
from load_dynamodb import save_dynamodb_table

app = Flask(__name__)

@app.route('/join', methods=['POST'])
def join():
    user_info = request.json
    
    # user_info를 데이터베이스에 저장
    try:
        dynamo_save_result = save_dynamodb_table(user_info, 'user')
        return jsonify({"message": "User registered successfully", "user": dynamo_save_result}), 201
    
    except Exception as e:
        return jsonify({"message": "User registration failed", "error": str(e)}), 500

@app.route('/trip', methods=['POST'])
def trip():
    trip_info = request.json
    
    # trip_info 데이터베이스에 저장 (+유효성 검사)
    try:
        dynamo_save_result = save_dynamodb_table(trip_info, 'trip')
        return jsonify({"message": "Trip data save successfully", "user": dynamo_save_result}), 201
    
    except Exception as e:
        return jsonify({"message": "Trip data save failed", "error": str(e)}), 500

@app.route('/experience', methods=['POST'])
def experience():
    experience_info = request.json
    
    # experience_info를 데이터베이스에 저장 (+유효성 검사)
    try:
        dynamo_save_result = save_dynamodb_table(experience_info, 'trip')
        return jsonify({"message": "Experience data save successfully", "user": dynamo_save_result}), 201
    
    except Exception as e:
        return jsonify({"message": "Experience data save failed", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30001)
