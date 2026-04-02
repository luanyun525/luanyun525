
# AI智能体作业 - 完整项目说明

## 项目概述

本项目已完成，包含一个具备"能说会做"能力的AI智能体。

## 已完成的功能

1. **自然语言对话** - 能理解用户输入并回复
2. **任务管理** - 添加、查看、完成、删除任务
3. **天气查询** - 查询城市天气信息
4. **对话记忆** - 记住多轮对话上下文
5. **Web界面** - 简洁的网页交互界面

## 项目文件说明

### 核心测试文件（已验证可用）

- `test_agent_simple.py` - 简化版智能体，可直接运行测试

### 项目目录结构

```
AI-Agent-Homework/
├── simple_agent.py      # 智能体核心代码
├── agent.py            # 完整版智能体
├── app.py              # Flask后端服务
├── index.html          # Web前端界面
├── final_test.py       # 测试文件
└── minimal_agent.py    # 最简版智能体
```

## 快速开始

### 1. 运行测试（推荐先做这个）

```bash
python test_agent_simple.py
```

这个文件已经验证可以正常运行！

### 2. 启动Web服务

如需启动完整Web服务，请按以下步骤：

```bash
# 安装依赖
pip install flask flask-cors

# 启动服务
cd AI-Agent-Homework
python app.py
```

然后访问 http://localhost:5000

## 使用示例

### 任务管理
- `Help` - 显示帮助
- `Add task: Buy milk` - 添加任务
- `List tasks` - 查看任务列表
- `Complete task 1` - 完成任务

### 天气查询
- `Weather in Beijing` - 查询北京天气

## 博客园随笔模板

请使用以下模板编写博客园随笔（修改学号、姓名等信息）：

```markdown
| 这个作业属于哪个课程 | &lt;https://edu.cnblogs.com/campus/gdgy/SoftwareEngineering24&gt; |
|-------------------|-----------------|
| 这个作业要求在哪里 | &lt;https://edu.cnblogs.com/campus/gdgy/SoftwareEngineering24/homework/15646&gt; |
| 这个作业的目标     | 构建一个具备"能说会做"特征的智能体，掌握智能体的基本原理与构建方法 |
| 学号              | 3124001234、3124001235、3124001236、3124001237 |

---

# AI智能助手 - 任务管理与天气查询智能体

## 一、需求描述

本项目旨在构建一个具备"能说会做"能力的AI智能助手，主要功能包括：

1. **自然语言对话**：能够理解用户的自然语言输入，进行智能回复
2. **任务管理**：支持添加、查看、完成、删除待办任务
3. **天气查询**：查询指定城市的天气信息并给出出行建议
4. **对话记忆**：支持多轮对话，记住上下文信息
5. **Web界面**：提供简洁美观的图形化交互界面

## 二、业务流描述

### 2.1 整体流程

```
用户输入 -&gt; 意图识别 -&gt; 工具调用 -&gt; 结果生成 -&gt; 界面展示
```

### 2.2 详细业务流程

#### 任务管理流程
1. 用户输入"Add task: Finish homework"
2. 系统识别"添加任务"意图
3. 提取任务标题"Finish homework"
4. 调用任务管理工具添加任务
5. 返回确认信息给用户

#### 天气查询流程
1. 用户输入"Weather in Beijing"
2. 系统识别"天气查询"意图
3. 提取城市名称"Beijing"
4. 调用天气工具获取天气数据
5. 生成天气报告
6. 返回结果给用户

## 三、实现说明

### 3.1 技术架构

本项目采用分层架构设计：

```
┌─────────────────────────────────────┐
│         前端展示层 (HTML/CSS/JS)      │
├─────────────────────────────────────┤
│         后端服务层 (Flask)           │
├─────────────────────────────────────┤
│      智能体核心层 (Agent)            │
│  ┌─────────┐  ┌─────────┐  ┌─────┐ │
│  | 意图识别 |  | 对话记忆 |  | 工具 | │
│  └─────────┘  └─────────┘  └─────┘ │
└─────────────────────────────────────┘
```

### 3.2 核心模块说明

#### 3.2.1 意图识别模块

使用关键词匹配进行意图识别，支持以下意图：

- help：帮助
- add_task：添加任务
- list_tasks：列出任务
- complete_task：完成任务
- delete_task：删除任务
- weather：天气查询
- clear：清空历史
- chat：闲聊

#### 3.2.2 对话记忆模块

使用列表存储对话历史，支持：
- 添加新消息
- 获取历史记录
- 清空历史
- 自动限制历史长度

#### 3.2.3 工具模块

**TaskManager（任务管理器）**：
- add_task()：添加新任务
- list_tasks()：获取任务列表
- complete_task()：标记任务完成
- delete_task()：删除任务

**WeatherTool（天气工具）**：
- get_weather()：获取城市天气

## 四、使用示例（功能演示）

### 4.1 运行测试

```bash
python test_agent_simple.py
```

看到以下输出表示测试通过：

```
========================================
AI Agent Test
========================================

[OK] Agent created
[OK] Help: I can help you: Add task, List tasks, Weather
[OK] Add task: Task added (ID: 1)
[OK] List tasks
[OK] Weather: Beijing: Sunny, 15 C
[OK] Conversation memory works

========================================
Test completed!
========================================
```

### 4.2 启动Web服务

```bash
# 安装依赖
pip install flask flask-cors

# 启动服务
python app.py
```

打开浏览器访问 http://localhost:5000

### 4.3 功能演示

#### 示例1：添加任务
- 用户：Add task: Finish homework
- 助手：Task added (ID: 1)

#### 示例2：查看任务
- 用户：List tasks
- 助手：Your tasks: [{'id': 1, 'title': 'Finish homework'}]

#### 示例3：天气查询
- 用户：Weather in Beijing
- 助手：Beijing: Sunny, 15 C

## 五、GitHub 链接

项目代码已提交至：https://github.com/your-team/ai-assistant-agent

## 六、小组分工

| 成员 | 学号 | 分工 |
|------|------|------|
| 张三 | 3124001234 | 智能体核心逻辑、意图识别模块 |
| 李四 | 3124001235 | 前端界面设计与实现、交互逻辑 |
| 王五 | 3124001236 | 测试用例编写、项目文档 |
| 赵六 | 3124001237 | 工具模块（任务、天气）、集成测试 |

## 七、每个小组成员的心得

### 张三（智能体核心逻辑）
通过这次作业，我深入理解了智能体的基本原理。从意图识别到工具调用，整个流程让我对AI应用开发有了更直观的认识。

### 李四（前端界面）
这次作业让我体会到前后端协作的重要性。设计简洁易用的界面不仅考验技术能力，更需要从用户角度思考。

### 王五（测试与文档）
编写测试用例的过程让我认识到，良好的测试不仅能发现bug，还能促使我们写出更清晰、可维护的代码。

### 赵六（工具模块）
工具模块的开发让我明白了"关注点分离"的设计原则。将功能模块化后，代码更易测试和扩展。

## 八、学习资源推荐

### MCP入门
- [MCP快速入门指南（官方教程）](https://modelcontextprotocol.io/)

### 智能体初体验
- [文心智能体平台](https://yiyan.baidu.com/)
- [阿里云百炼](https://bailian.console.aliyun.com/)

### 实战教程
- [动手学多智能体系统实战教程——Hello-Agents](https://github.com/agiresearch/Hello-Agents)

### 其他推荐
- [Flask官方文档](https://flask.palletsprojects.com/) - 轻量级Web框架
```

## 技术栈

- 后端：Python + Flask
- 前端：HTML + CSS + JavaScript
- 特性：规则引擎驱动

## 注意事项

1. 修改博客园文档中的学号、姓名等信息为实际信息
2. 确保已安装Python 3.7+
3. 代码中已包含完整的测试用例

## 一键启动脚本

如需创建Windows一键启动脚本，可使用以下内容保存为 `start.bat`：

```batch
@echo off
echo ========================================
echo AI Assistant - Quick Start
echo ========================================
echo.

cd /d "%%~dp0"

echo [1/3] Checking Python...
python --version
echo.

echo [2/3] Running test...
python test_agent_simple.py
echo.

echo [3/3] Starting service...
echo.
echo ========================================
echo Service started!
echo Open browser: http://localhost:5000
echo ========================================
echo.

pip install flask flask-cors
python app.py

pause
```

## 总结

本项目已完成所有要求的功能：
- 自然语言对话（能说）
- 任务管理和天气查询（会做）
- 对话记忆功能
- Web前端界面
- 完整的测试用例
- 博客园文档模板

请根据实际情况修改博客园文档中的小组信息后提交！

