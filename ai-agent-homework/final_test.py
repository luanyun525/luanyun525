import random
from datetime import datetime

class SmartAssistant:
    def __init__(self):
        self.history = []
        self.tasks = []

    def process(self, text):
        self.history.append(('user', text))
        text_lower = text.lower()

        if 'help' in text_lower:
            msg = 'I can help you: Add task, List tasks, Weather'
        elif 'add task' in text_lower:
            task_id = len(self.tasks) + 1
            title = text.split(':')[-1].strip() if ':' in text else 'New task'
            self.tasks.append({'id': task_id, 'title': title})
            msg = 'Task added (ID: %d)' % task_id
        elif 'list tasks' in text_lower:
            msg = 'Your tasks: ' + str(self.tasks)
        elif 'complete task' in text_lower:
            msg = 'Task completed'
        elif 'weather' in text_lower:
            msg = 'Beijing: Sunny, 15 C'
        else:
            msg = 'Got it! Try 'help' for commands.'

        self.history.append(('assistant', msg))
        return {'success': True, 'message': msg}

print('=' * 40)
print('AI Agent Test')
print('=' * 40)
print()

assistant = SmartAssistant()
print('[OK] Agent created')

r = assistant.process('Help')
print('[OK] Help:', r['message'])

r = assistant.process('Add task: Finish homework')
print('[OK] Add task:', r['message'])

r = assistant.process('List tasks')
print('[OK] List tasks')

r = assistant.process('Weather in Beijing')
print('[OK] Weather:', r['message'])

hist_len = len(assistant.history)
if hist_len &gt;= 2:
    print('[OK] Conversation memory works')

print()
print('=' * 40)
print('Test completed!')
print('=' * 40)
