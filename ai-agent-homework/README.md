# AI Assistant - Intelligent Agent Project

An AI agent with "talk and act" capabilities, supporting task management, weather queries, and natural language conversation.

## Features

- **Natural Language Conversation**: Understand user intent and chat intelligently
- **Task Management**: Add, list, complete, and delete tasks
- **Weather Query**: Get weather information for cities
- **Conversation Memory**: Remember context across multiple turns
- **Web Interface**: Clean and beautiful frontend UI

## Quick Start

### Method 1: One-click Start (Recommended)

Windows:
```bash
Double-click: start.bat
```

Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

### Method 2: Manual Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
python tests/test_agent.py
```

3. Start service:
```bash
cd agent
python app.py
```

4. Open browser:
Visit http://localhost:5000

## Usage Examples

### Task Management
- "add task: Finish homework"
- "list tasks"
- "complete task 1"
- "delete task 1"

### Weather Query
- "weather in Beijing"
- "Shanghai weather"

### Other
- "help" - See usage instructions
- "clear history" - Clear conversation history

## Project Structure

```
ai-agent-homework/
├── agent/
│   ├── __init__.py       # Package init
│   ├── agent.py          # Core agent logic
│   ├── memory.py         # Conversation memory
│   ├── tools.py          # Tools (tasks, weather)
│   └── app.py            # Flask backend
├── frontend/
│   └── index.html        # Frontend UI
├── tests/
│   ├── __init__.py
│   └── test_agent.py     # Test cases
├── requirements.txt      # Python dependencies
├── README.md            # Project README
├── start.bat            # Windows quick start
└── start.sh             # Linux/Mac quick start
```

## Tech Stack

- Backend: Python + Flask
- Frontend: HTML + CSS + JavaScript
- No external AI API dependencies, built-in rule engine

## Team Members

- Student 1: Core agent logic and intent recognition
- Student 2: Frontend UI design and implementation
- Student 3: Test cases and documentation
- Student 4: Tool modules and integration

## Learning Resources

- [MCP Quick Start Guide](https://modelcontextprotocol.io/)
- [Hello-Agents Tutorial](https://github.com/agiresearch/Hello-Agents)
- [Flask Documentation](https://flask.palletsprojects.com/)

## GitHub Repository

https://github.com/luanyun525/luanyun525
