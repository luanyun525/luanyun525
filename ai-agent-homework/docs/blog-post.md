| This assignment belongs to | <https://edu.cnblogs.com/campus/gdgy/SoftwareEngineering24> |
|----------------------------|-----------------|
| Where to find requirements | <https://edu.cnblogs.com/campus/gdgy/SoftwareEngineering24/homework/15646> |
| Assignment goal            | Build an intelligent agent with "talk and act" capabilities, master basic principles and construction methods of agents |
| Student IDs                | 3124001234, 3124001235, 3124001236, 3124001237 |

---

# AI Assistant - Task Management and Weather Query Intelligent Agent

## 1. Requirement Description

This project aims to build an AI intelligent assistant with "talk and act" capabilities. The main functions include:

1. **Natural Language Conversation**: Understand user's natural language input and provide intelligent responses
2. **Task Management**: Support adding, viewing, completing, and deleting todo tasks
3. **Weather Query**: Query weather information for specified cities and provide travel suggestions
4. **Conversation Memory**: Support multi-turn conversations, remembering context information
5. **Web Interface**: Provide a clean and beautiful graphical interaction interface

## 2. Business Flow Description

### 2.1 Overall Flow

```
User Input -> Intent Recognition -> Tool Call -> Result Generation -> UI Display
```

### 2.2 Detailed Business Flow

#### Task Management Flow
1. User inputs "add task: Finish homework"
2. System recognizes "add_task" intent
3. Extracts task title "Finish homework"
4. Calls task management tool to add task
5. Returns confirmation message to user

#### Weather Query Flow
1. User inputs "weather in Beijing"
2. System recognizes "weather" intent
3. Extracts city name "Beijing"
4. Calls weather tool to get weather data
5. Generates weather report and travel suggestions
6. Returns results to user

## 3. Implementation Description

### 3.1 Technical Architecture

This project uses layered architecture design:

```
Frontend Layer (HTML/CSS/JS)
    |
Backend Service Layer (Flask)
    |
Agent Core Layer (Agent)
    |-- Intent Recognition
    |-- Conversation Memory
    |-- Tools (Tasks, Weather)
```

### 3.2 Core Modules

**Intent Recognition**: Uses regex patterns to identify user intents
**Conversation Memory**: Stores conversation history with auto-truncation
**Task Manager**: Manages todo tasks with CRUD operations
**Weather Tool**: Provides weather information and travel advice

### 3.3 Key Features

- **Intent Detection**: add_task, list_tasks, complete_task, delete_task, weather, help, clear, chat
- **Multi-turn Memory**: Remembers conversation context
- **Web UI**: Beautiful gradient design with quick action buttons
- **No External APIs**: Built-in rule engine, works offline

## 4. Usage Examples

### Starting the Service

Double-click `start.bat` (Windows) or run `./start.sh` (Linux/Mac)

### Function Demo

- **Add Task**: "add task: Finish software engineering homework"
- **List Tasks**: "list tasks"
- **Weather**: "weather in Beijing"
- **Complete Task**: "complete task 1"
- **Help**: "help"

## 5. GitHub Link

https://github.com/luanyun525/luanyun525

## 6. Team Division

| Member | Student ID | Responsibilities |
|--------|------------|------------------|
| Member 1 | 3124001234 | Core agent logic, intent recognition |
| Member 2 | 3124001235 | Frontend UI design and implementation |
| Member 3 | 3124001236 | Test cases and project documentation |
| Member 4 | 3124001237 | Tool modules, integration testing |

## 7. Learning Resources

- [MCP Quick Start Guide](https://modelcontextprotocol.io/)
- [Hello-Agents Tutorial](https://github.com/agiresearch/Hello-Agents)
- [Flask Documentation](https://flask.palletsprojects.com/)
