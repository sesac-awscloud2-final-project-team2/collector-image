from flask import Flask, request, jsonify
import os
# from load_dynamodb import save_dynamodb_table
from dotenv import load_dotenv

load_dotenv()

collector_port = os.getenv('COLLECTOR_PORT')
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "hello world"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=collector_port)
