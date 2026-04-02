from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from agent import SmartAssistant
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, static_folder="../frontend")
CORS(app)

assistant = SmartAssistant()


@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"success": False, "message": "Please input message"}), 400
    response = assistant.process(user_input)
    return jsonify(response)


@app.route("/api/history", methods=["GET"])
def history():
    return jsonify({"history": assistant.get_history()})


@app.route("/api/clear", methods=["POST"])
def clear():
    assistant.memory.clear()
    return jsonify({"success": True, "message": "Cleared"})


if __name__ == "__main__":
    print("=" * 50)
    print("AI Assistant Service Starting...")
    print("Visit: http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
