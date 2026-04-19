"""AI 学习伴侣 - 对话记忆模块"""

from datetime import datetime

from .config import MAX_HISTORY


class ConversationMemory:
    """对话记忆管理，支持滑动窗口和 OpenAI 格式输出"""

    def __init__(self, max_history: int = MAX_HISTORY):
        self.history = []
        self.max_history = max_history

    def add_message(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self) -> list:
        return self.history

    def get_openai_messages(self) -> list:
        """返回符合 OpenAI API 格式的消息列表（仅 role + content）"""
        return [{"role": m["role"], "content": m["content"]} for m in self.history]

    def clear(self):
        self.history = []
