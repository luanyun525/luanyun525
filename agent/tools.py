"""AI 学习伴侣 - 工具模块（任务管理 + 天气查询）"""

import json
import logging
from datetime import datetime

import requests

from .config import DATA_DIR, TASKS_FILE

logger = logging.getLogger(__name__)


class TaskManager:
    """任务管理工具"""

    def __init__(self):
        self.tasks = []
        self._next_id = 1
        self._load()

    def add_task(self, title: str, description: str = "", priority: str = "medium") -> dict:
        task = {
            "id": self._next_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
        }
        self._next_id += 1
        self.tasks.append(task)
        self._save()
        return task

    def list_tasks(self, status: str = None) -> list:
        if status:
            return [t for t in self.tasks if t["status"] == status]
        return list(self.tasks)

    def complete_task(self, task_id: int):
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                self._save()
                return {"success": True, "task_id": task_id, "message": f"任务 {task_id} 已完成"}
        return {"success": False, "error": f"未找到任务 {task_id}"}

    def delete_task(self, task_id: int):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                removed = self.tasks.pop(i)
                self._save()
                return {"success": True, "task_id": task_id, "message": f"已删除任务: {removed['title']}"}
        return {"success": False, "error": f"未找到任务 {task_id}"}

    def _save(self):
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = {"next_id": self._next_id, "tasks": self.tasks}
            TASKS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            logger.warning("任务数据保存失败: %s", e)

    def _load(self):
        try:
            if TASKS_FILE.exists():
                data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
                self.tasks = data.get("tasks", [])
                self._next_id = data.get("next_id", len(self.tasks) + 1)
        except Exception as e:
            logger.warning("任务数据加载失败: %s", e)


class WeatherTool:
    """天气查询工具 - 使用 wttr.in 免费 API"""

    def get_weather(self, city: str) -> dict:
        try:
            url = f"https://wttr.in/{city}?format=j1"
            resp = requests.get(url, timeout=8, headers={"Accept-Language": "zh-CN"})
            resp.raise_for_status()
            data = resp.json()
            current = data["current_condition"][0]
            temp = int(current["temp_C"])
            condition = current.get("lang_zh", [{}])[0].get("value", current["weatherDesc"][0]["value"])
            humidity = int(current["humidity"])
            wind_speed = current["windspeedKmph"]
            feels_like = int(current["FeelsLikeC"])

            return {
                "city": city,
                "temperature": temp,
                "feels_like": feels_like,
                "condition": condition,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "advice": self._get_advice(temp, condition),
            }
        except requests.RequestException as e:
            logger.warning("天气查询失败 (%s): %s", city, e)
            return {
                "city": city,
                "error": f"无法获取 {city} 的天气信息，请检查城市名称是否正确",
            }
        except Exception as e:
            logger.error("天气数据解析失败: %s", e)
            return {"city": city, "error": "天气数据解析失败"}

    def _get_advice(self, temp: int, condition: str) -> str:
        tips = []
        if temp < 10:
            tips.append("天气寒冷，注意保暖，建议穿厚外套")
        elif temp < 20:
            tips.append("气温适中偏凉，建议穿薄外套或长袖")
        elif temp > 30:
            tips.append("天气炎热，注意防暑降温，多喝水")
        else:
            tips.append("气温舒适，适合户外活动")

        condition_lower = condition.lower() if condition else ""
        if "雨" in condition_lower or "rain" in condition_lower:
            tips.append("有降雨，记得带伞")
        elif "雪" in condition_lower or "snow" in condition_lower:
            tips.append("有降雪，路面可能湿滑，出行注意安全")

        return "；".join(tips)
