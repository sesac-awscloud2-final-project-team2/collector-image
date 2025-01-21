from flask import Flask, request, jsonify
import os
from load_dynamodb import save_dynamodb_table
from dotenv import load_dotenv

load_dotenv()

collector_port = os.getenv('COLLECTOR_PORT')
app = Flask(__name__)

@app.route('/join', methods=['POST'])
def join():
    user_info = request.json
    
    # user_info를 데이터베이스에 저장 (+유효성 검사)
    try:
        save_dynamodb_table(user_info, 'user')
        return jsonify({"message": "User registered successfully", "user": user_info}), 201
    
    except Exception as e:
        return jsonify({"message": "User registration failed", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=collector_port)
