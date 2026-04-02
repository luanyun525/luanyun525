
import re
import random
from .memory import ConversationMemory
from .tools import TaskManager, WeatherTool

class SmartAssistant:
    def __init__(self):
        self.memory = ConversationMemory()
        self.task_manager = TaskManager()
        self.weather_tool = WeatherTool()
        self.intent_patterns = {
            "add_task": [
                r"add task[:\s]*(.+)",
                r"create task[:\s]*(.+)",
                r"new task[:\s]*(.+)",
                r"remember[:\s]*(.+)",
            ],
            "list_tasks": [
                r"list tasks",
                r"show tasks",
                r"my tasks",
                r"what tasks",
            ],
            "complete_task": [
                r"complete task[\s]*(\d+)",
                r"mark task[\s]*(\d+)[\s]*complete",
            ],
            "delete_task": [
                r"delete task[\s]*(\d+)",
            ],
            "weather": [
                r"weather in (.+)",
                r"(.+) weather",
                r"how is weather in (.+)",
            ],
            "help": [
                r"help",
                r"what can you do",
                r"how to use",
            ],
            "clear": [
                r"clear history",
                r"clear conversation",
                r"reset",
            ]
        }

    def process(self, user_input):
        self.memory.add_message("user", user_input)
        intent = self._detect_intent(user_input.lower())
        response = self._execute_intent(intent, user_input)
        self.memory.add_message("assistant", response["message"])
        return response

    def _detect_intent(self, text):
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return intent
        return "chat"

    def _execute_intent(self, intent, text):
        if intent == "add_task":
            return self._handle_add_task(text)
        elif intent == "list_tasks":
            return self._handle_list_tasks()
        elif intent == "complete_task":
            return self._handle_complete_task(text)
        elif intent == "delete_task":
            return self._handle_delete_task(text)
        elif intent == "weather":
            return self._handle_weather(text)
        elif intent == "help":
            return self._handle_help()
        elif intent == "clear":
            return self._handle_clear()
        else:
            return self._handle_chat(text)

    def _handle_add_task(self, text):
        for pattern in self.intent_patterns["add_task"]:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                if title:
                    task = self.task_manager.add_task(title)
                    return {
                        "success": True,
                        "action": "add_task",
                        "data": task,
                        "message": "Task added: %s (ID: %d)" % (task['title'], task['id'])
                    }
        return {"success": False, "message": "Please tell me the task content"}

    def _handle_list_tasks(self):
        tasks = self.task_manager.list_tasks()
        if not tasks:
            return {"success": True, "action": "list_tasks", "data": [], "message": "No tasks yet"}
        message = "Your tasks:\n"
        for task in tasks:
            status = "[X]" if task["status"] == "completed" else "[ ]"
            message += "%s %d. %s\n" % (status, task['id'], task['title'])
        return {"success": True, "action": "list_tasks", "data": tasks, "message": message}

    def _handle_complete_task(self, text):
        match = re.search(r"(\d+)", text)
        if match:
            task_id = int(match.group(1))
            if self.task_manager.complete_task(task_id):
                return {"success": True, "action": "complete_task", "data": {"task_id": task_id}, "message": "Task %d marked as complete" % task_id}
        return {"success": False, "message": "Task not found"}

    def _handle_delete_task(self, text):
        match = re.search(r"(\d+)", text)
        if match:
            task_id = int(match.group(1))
            if self.task_manager.delete_task(task_id):
                return {"success": True, "action": "delete_task", "data": {"task_id": task_id}, "message": "Task %d deleted" % task_id}
        return {"success": False, "message": "Task not found"}

    def _handle_weather(self, text):
        match = re.search(r"(?:weather in|how is weather in)\s+(.+)", text, re.IGNORECASE)
        if not match:
            match = re.search(r"(.+)\s+weather", text, re.IGNORECASE)
        if match:
            city = match.group(1).strip()
            weather = self.weather_tool.get_weather(city)
            message = "%s: %s, %dC, %d%% humidity\nAdvice: %s" % (weather['city'], weather['condition'], weather['temperature'], weather['humidity'], weather['advice'])
            return {"success": True, "action": "weather", "data": weather, "message": message}
        return {"success": False, "message": "Please specify a city (e.g., 'weather in Beijing')"}

    def _handle_help(self):
        help_text = """I can help you with:
- Task Management
  * "add task: Buy milk"
  * "list tasks"
  * "complete task 1"
  * "delete task 1"

- Weather
  * "weather in Beijing"

- General Chat
  * Just talk to me!

Try "help" anytime!"""
        return {"success": True, "action": "help", "message": help_text}

    def _handle_clear(self):
        self.memory.clear()
        return {"success": True, "action": "clear", "message": "Conversation history cleared"}

    def _handle_chat(self, text):
        responses = [
            "Got it! How can I help you? Try 'help' to see what I can do!",
            "OK, I understand. Try asking me to add a task or check the weather!",
            "Hmm, interesting! Is there something specific I can help with?",
        ]
        return {"success": True, "action": "chat", "message": random.choice(responses)}

    def get_history(self):
        return self.memory.get_history()

