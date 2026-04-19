"""AI 学习伴侣 - Flask Web 服务"""

import json
import logging
import os
import sys
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from flask_cors import CORS

# 确保项目根目录在 sys.path 中
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agent.config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, KIMI_API_KEY

app = Flask(__name__, static_folder=str(PROJECT_ROOT / "frontend"))
CORS(app)

# 延迟初始化智能体（避免 import 时就要求 API Key）
assistant = None


def get_assistant():
    global assistant
    if assistant is None:
        if not KIMI_API_KEY:
            raise ValueError("未配置 KIMI_API_KEY，请在 .env 文件中设置")
        from agent.agent import SmartAssistant
        assistant = SmartAssistant()
    return assistant


@app.route("/")
def index():
    return send_from_directory(str(PROJECT_ROOT / "frontend"), "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """非流式对话接口"""
    data = request.json or {}
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"success": False, "message": "请输入消息内容"}), 400

    try:
        agent = get_assistant()
        response = agent.process(user_input)
        return jsonify(response)
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        logging.error("对话处理失败: %s", e)
        return jsonify({"success": False, "message": "服务内部错误"}), 500


@app.route("/api/chat/stream", methods=["POST"])
def chat_stream():
    """SSE 流式对话接口"""
    data = request.json or {}
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"success": False, "message": "请输入消息内容"}), 400

    try:
        agent = get_assistant()
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 500

    def generate():
        try:
            for chunk in agent.process_stream(user_input):
                payload = json.dumps({"content": chunk}, ensure_ascii=False)
                yield f"data: {payload}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logging.error("流式输出异常: %s", e)
            error_payload = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"data: {error_payload}\n\n"
            yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@app.route("/api/history", methods=["GET"])
def history():
    try:
        agent = get_assistant()
        return jsonify({"success": True, "history": agent.get_history()})
    except ValueError:
        return jsonify({"success": True, "history": []})


@app.route("/api/clear", methods=["POST"])
def clear():
    try:
        agent = get_assistant()
        agent.memory.clear()
        return jsonify({"success": True, "message": "对话历史已清空"})
    except ValueError:
        return jsonify({"success": True, "message": "对话历史已清空"})


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """获取任务列表（供前端侧边栏使用）"""
    try:
        agent = get_assistant()
        tasks = agent.task_manager.list_tasks()
        return jsonify({"success": True, "tasks": tasks})
    except ValueError:
        return jsonify({"success": True, "tasks": []})


if __name__ == "__main__":
    print("=" * 50)
    print("  AI 学习伴侣 - 服务启动中...")
    print(f"  访问地址: http://localhost:{FLASK_PORT}")
    print("=" * 50)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
