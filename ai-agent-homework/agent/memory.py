
from datetime import datetime

class ConversationMemory:
    def __init__(self, max_history=20):
        self.history = []
        self.max_history = max_history

    def add_message(self, role, content):
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []

