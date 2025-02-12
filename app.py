from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram
import time

from load_dynamodb import save_dynamodb_table

app = Flask(__name__)
metrics = PrometheusMetrics(app)
# metrics.info('app_info', 'Application info', version='1.0')

# 요청 횟수를 측정하는 Counter 정의
request_counter = Counter(
    'by_path_counter', 'Request count by request paths',
    ['path']
)

# 요청 처리 시간을 측정하는 Histogram 정의
request_duration = Histogram(
    'http_request_duration_seconds', 'Request processing time',
    ['path']
)


@app.route('/join', methods=['POST'])
def join():
    start_time = time.time()  # :hourglass_flowing_sand: 요청 시작 시간 기록
    request_counter.labels(path=request.path).inc()
    user_info = request.json
    
    # user_info를 데이터베이스에 저장
    try:
        dynamo_save_result = save_dynamodb_table(user_info, 'user')
        request_duration.labels(path=request.path).observe(time.time() - start_time)  # :hourglass_flowing_sand: 응>답 시간 기록
        return jsonify({"message": "User registered successfully", "user": dynamo_save_result}), 201
    
    except Exception as e:
        return jsonify({"message": "User registration failed", "error": str(e)}), 500

@app.route('/trip', methods=['POST'])
def trip():
    start_time = time.time()
    request_counter.labels(path=request.path).inc()
    trip_info = request.json
    
    # trip_info 데이터베이스에 저장 (+유효성 검사)
    try:
        dynamo_save_result = save_dynamodb_table(trip_info, 'trip')
        request_duration.labels(path=request.path).observe(time.time() - start_time)
        return jsonify({"message": "Trip data save successfully", "user": dynamo_save_result}), 201
    
    except Exception as e:
        return jsonify({"message": "Trip data save failed", "error": str(e)}), 500

@app.route('/experience', methods=['POST'])
def experience():
    start_time = time.time()
    request_counter.labels(path=request.path).inc()
    experience_info = request.json
    
    # experience_info를 데이터베이스에 저장 (+유효성 검사)
    try:
        dynamo_save_result = save_dynamodb_table(experience_info, 'experience')
        request_duration.labels(path=request.path).observe(time.time() - start_time)
        return jsonify({"message": "Experience data save successfully", "user": dynamo_save_result}), 201
    
    except Exception as e:
        return jsonify({"message": "Experience data save failed", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30001)
