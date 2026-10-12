import os

from flask import Flask, request, jsonify
from src.services.phishing_service import analyze_url
from src.services.message_service import analyze_message


app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "phishing-detection-api",
        "status": "ok",
        "endpoints": ["/health", "/predict", "/predict/message"],
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():

    if request.method == "OPTIONS":
        return jsonify({}), 200

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        url = data.get("url")

        if not url:
            return jsonify({
                "error": "URL is required"
            }), 400

        result = analyze_url(url)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/predict/message", methods=["POST", "OPTIONS"])
def predict_message():

    if request.method == "OPTIONS":
        return jsonify({}), 200

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        message = data.get("message")

        if not message:
            return jsonify({
                "error": "Message is required"
            }), 400

        result = analyze_message(message)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
