import os
import boto3
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:8000", "http://127.0.0.1:8000"]}})

# AWS S3 setup
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")
)
S3_BUCKET = os.getenv("S3_BUCKET_NAME")

# Store results temporarily in memory (for demo purposes)
results_cache = {}

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        field = request.form.get("field")
        file = request.files.get("cv")

        if not all([name, email, field, file]):
            return jsonify({"error": "Missing required fields"}), 400

        filename = secure_filename(file.filename)
        s3_path = f"uploads/{filename}"
        file.seek(0)
        s3.upload_fileobj(file, S3_BUCKET, s3_path)
        file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_path}"

        # Generate an ID for this submission to track result
        submission_id = email  # for simplicity, can use uuid.uuid4()
        results_cache[submission_id] = None  # placeholder

        payload = {
            "name": name,
            "email": email,
            "field": field,
            "cv_url": file_url,
            "submission_id": submission_id  # send this to n8n
        }

        # Send payload to n8n webhook
        import requests
        N8N_WEBHOOK_URL = "http://34.201.128.243:5678/webhook-test/webhook-test/1d91fb1e-ff37-41ba-bf8c-de969b185078"
        res = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=120)

        return jsonify({"message": "Workflow triggered", "submission_id": submission_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/receive-result', methods=['POST'])
def receive_result():
    try:
        data = request.get_json()
        submission_id = data.get("submission_id")
        if not submission_id:
            return jsonify({"error": "Missing submission_id"}), 400

        # Store the result
        results_cache[submission_id] = {
            "score": data.get("score"),
            "feedback": data.get("feedback")
        }

        print(f">>> Received result for {submission_id}: {results_cache[submission_id]}")

        return jsonify({"message": "Result received"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get-result/<submission_id>', methods=['GET'])
def get_result(submission_id):
    result = results_cache.get(submission_id)
    if result is None:
        return jsonify({"status": "pending"}), 200
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5678)
