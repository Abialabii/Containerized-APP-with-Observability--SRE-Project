from flask import Flask, render_template, jsonify
from prometheus_client import Counter, Histogram, generate_latest
import time
import random

app = Flask(__name__)

# Prometheus metrics instrumentation
REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('app_request_duration_seconds', 'Request duration')

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    with REQUEST_DURATION.time():
        # Simulate processing time
        time.sleep(random.uniform(0.1, 0.3))
        return render_template('index.html')

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    return jsonify({"status": "healthy"})

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
