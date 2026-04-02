
from datetime import datetime
import random

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description="", priority="medium"):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        return task

    def list_tasks(self, status=None):
        if status:
            return [t for t in self.tasks if t["status"] == status]
        return self.tasks

    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                return True
        return False

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(i)
                return True
        return False

class WeatherTool:
    def __init__(self):
        pass

    def get_weather(self, city):
        temp = random.randint(10, 30)
        conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]
        condition = random.choice(conditions)
        humidity = random.randint(40, 80)
        return {
            "city": city,
            "temperature": temp,
            "condition": condition,
            "humidity": humidity,
            "advice": self._get_advice(temp, condition)
        }

    def _get_advice(self, temp, condition):
        advice = []
        if temp < 15:
            advice.append("Wear warm clothes")
        elif temp > 25:
            advice.append("Stay cool and hydrated")
        if "Rain" in condition:
            advice.append("Don't forget your umbrella")
        return "; ".join(advice) if advice else "Great weather for outdoor activities!"

