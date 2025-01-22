from flask import Flask, request, jsonify
from load_dynamodb import save_dynamodb_table, collector_port

app = Flask(__name__)

@app.route('/join', methods=['POST'])
def join():
    user_info = request.json
    
    # user_info를 데이터베이스에 저장 (+유효성 검사)
    try:
        dynamo_save_result = save_dynamodb_table(user_info, 'join')
        return jsonify({"message": "User registered successfully", "user": dynamo_save_result}), 201
    
    except Exception as e:
        return jsonify({"message": "User registration failed", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=collector_port)
