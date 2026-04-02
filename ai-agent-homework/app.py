
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import SmartAssistant

app = Flask(__name__, static_folder='.')
CORS(app)

assistant = SmartAssistant()


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    if not user_input:
        return jsonify({'success': False, 'message': 'Please enter a message'}), 400
    response = assistant.process(user_input)
    return jsonify(response)


@app.route('/api/history', methods=['GET'])
def history():
    return jsonify({'history': assistant.get_history()})


if __name__ == '__main__':
    print('Starting AI Assistant service...')
    print('Visit: http://localhost:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)

