"""AI 学习伴侣 - 配置管理模块"""

import os
from pathlib import Path

# 尝试加载 .env 文件
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass


# DeepSeek API 配置（兼容 OpenAI 格式）
KIMI_API_KEY = os.environ.get("KIMI_API_KEY", "")
KIMI_BASE_URL = os.environ.get("KIMI_BASE_URL", "https://api.deepseek.com")
KIMI_MODEL = os.environ.get("KIMI_MODEL", "deepseek-chat")

# Flask 服务配置
FLASK_HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.environ.get("PORT", os.environ.get("FLASK_PORT", 5000)))
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

# 数据目录
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TASKS_FILE = DATA_DIR / "tasks.json"
HISTORY_FILE = DATA_DIR / "history.json"

# 对话记忆配置
MAX_HISTORY = int(os.environ.get("MAX_HISTORY", 20))

# System Prompt
SYSTEM_PROMPT = """你是一个名为"AI 学习伴侣"的智能学习助手，专门帮助大学生管理学习任务和日常生活。

你的能力包括：
1. 任务管理：添加、查看、完成、删除学习待办任务
2. 天气查询：查询城市天气，给出出行建议
3. 学习建议：回答学习相关问题，制定学习计划
4. 日常对话：友好地与用户交流

回答规则：
- 用中文回复，语言亲切自然
- 处理复杂问题时，先用【思考】标注你的分析过程，再用【回答】给出最终回复
- 调用工具时不需要额外解释，直接给出结果即可
- 如果用户请求涉及任务操作或天气查询，请使用提供的工具来完成
"""
