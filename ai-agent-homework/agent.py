
import re
import random
from datetime import datetime


class ConversationMemory:
    def __init__(self, max_history=20):
        self.history = []
        self.max_history = max_history

    def add_message(self, role, content):
        self.history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        if len(self.history) &gt; self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title):
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        self.tasks.append(task)
        return task

    def list_tasks(self):
        return self.tasks

    def complete_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = 'completed'
                return True
        return False

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                self.tasks.pop(i)
                return True
        return False


class WeatherTool:
    def get_weather(self, city):
        data = {
            'Beijing': {'temp': 15, 'condition': 'Sunny', 'humidity': 45},
            'Shanghai': {'temp': 20, 'condition': 'Cloudy', 'humidity': 60},
            'Guangzhou': {'temp': 25, 'condition': 'Rainy', 'humidity': 75},
        }
        w = data.get(city, {'temp': 18, 'condition': 'Sunny', 'humidity': 50})
        return {
            'city': city,
            'temperature': w['temp'],
            'condition': w['condition'],
            'humidity': w['humidity']
        }


class SmartAssistant:
    def __init__(self):
        self.memory = ConversationMemory()
        self.task_manager = TaskManager()
        self.weather_tool = WeatherTool()

    def process(self, user_input):
        self.memory.add_message('user', user_input)
        response = self._handle_input(user_input)
        self.memory.add_message('assistant', response['message'])
        return response

    def _handle_input(self, text):
        text_lower = text.lower()

        if 'help' in text_lower:
            return self._help()
        elif 'add task' in text_lower:
            return self._add_task(text)
        elif 'list tasks' in text_lower:
            return self._list_tasks()
        elif 'complete task' in text_lower:
            return self._complete_task(text)
        elif 'delete task' in text_lower:
            return self._delete_task(text)
        elif 'weather' in text_lower:
            return self._weather(text)
        elif 'clear' in text_lower:
            return self._clear()
        else:
            return self._chat(text)

    def _help(self):
        msg = 'I can help you:\n- Add task: \'Add task: Buy milk\'\n- List tasks: \'List tasks\'\n- Complete task: \'Complete task 1\'\n- Weather: \'Weather in Beijing\'\n- Help: \'Help\''
        return {'success': True, 'action': 'help', 'message': msg}

    def _add_task(self, text):
        match = re.search(r'[:]\s*(.+)', text)
        if match:
            title = match.group(1).strip()
            task = self.task_manager.add_task(title)
            return {'success': True, 'action': 'add_task', 'message': 'Task added: %s (ID: %d)' % (task['title'], task['id'])}
        return {'success': False, 'message': 'Please specify task content'}

    def _list_tasks(self):
        tasks = self.task_manager.list_tasks()
        if not tasks:
            return {'success': True, 'action': 'list_tasks', 'message': 'No tasks'}
        msg = 'Your tasks:\n'
        for t in tasks:
            status = '[x]' if t['status'] == 'completed' else '[ ]'
            msg += '%s %d. %s\n' % (status, t['id'], t['title'])
        return {'success': True, 'action': 'list_tasks', 'message': msg}

    def _complete_task(self, text):
        match = re.search(r'(\d+)', text)
        if match:
            tid = int(match.group(1))
            if self.task_manager.complete_task(tid):
                return {'success': True, 'action': 'complete_task', 'message': 'Task %d completed' % tid}
        return {'success': False, 'message': 'Task not found'}

    def _delete_task(self, text):
        match = re.search(r'(\d+)', text)
        if match:
            tid = int(match.group(1))
            if self.task_manager.delete_task(tid):
                return {'success': True, 'action': 'delete_task', 'message': 'Task %d deleted' % tid}
        return {'success': False, 'message': 'Task not found'}

    def _weather(self, text):
        cities = ['Beijing', 'Shanghai', 'Guangzhou']
        for city in cities:
            if city in text:
                w = self.weather_tool.get_weather(city)
                msg = '%s: %s, %d C, humidity %d%%' % (w['city'], w['condition'], w['temperature'], w['humidity'])
                return {'success': True, 'action': 'weather', 'message': msg}
        return {'success': False, 'message': 'Try: Beijing, Shanghai, or Guangzhou'}

    def _clear(self):
        self.memory.clear()
        return {'success': True, 'action': 'clear', 'message': 'History cleared'}

    def _chat(self, text):
        responses = ['Got it! Try \'help\' to see what I can do.', 'OK! You can ask me to add tasks or check weather.', 'Hi there! Need any help?']
        return {'success': True, 'action': 'chat', 'message': random.choice(responses)}

    def get_history(self):
        return self.memory.get_history()


def run_test():
    print('=' * 40)
    print('AI Agent Test')
    print('=' * 40)
    print()

    try:
        assistant = SmartAssistant()
        print('[OK] Agent created')
    except Exception as e:
        print('[FAIL] Agent creation:', e)
        return False

    try:
        r = assistant.process('Help')
        print('[OK] Help command works')
    except Exception as e:
        print('[FAIL] Help command:', e)

    try:
        r = assistant.process('Add task: Finish homework')
        print('[OK] Add task works:', r['message'])
    except Exception as e:
        print('[FAIL] Add task:', e)

    try:
        r = assistant.process('List tasks')
        print('[OK] List tasks works')
    except Exception as e:
        print('[FAIL] List tasks:', e)

    try:
        r = assistant.process('Complete task 1')
        print('[OK] Complete task works:', r['message'])
    except Exception as e:
        print('[FAIL] Complete task:', e)

    try:
        r = assistant.process('Weather in Beijing')
        print('[OK] Weather query works:', r['message'])
    except Exception as e:
        print('[FAIL] Weather query:', e)

    try:
        history = assistant.get_history()
        if len(history) &gt;= 2:
            print('[OK] Conversation memory works')
    except Exception as e:
        print('[FAIL] Conversation memory:', e)

    print()
    print('=' * 40)
    print('Test completed!')
    print('=' * 40)
    return True


if __name__ == '__main__':
    run_test()

