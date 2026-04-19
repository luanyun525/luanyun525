# AI 学习伴侣 - 智能学业助手

基于 Kimi（月之暗面）大语言模型的智能学习助手，支持自然语言对话、任务管理、天气查询等功能。

## 功能特性

- **智能对话**：接入 Kimi 大语言模型，理解自然语言，流畅对话
- **Function Calling**：AI 自主调用工具（任务管理、天气查询）
- **流式输出**：打字机效果，实时显示 AI 回复
- **思维链可视化**：展示 AI 的推理过程
- **任务管理**：添加、查看、完成、删除待办任务（数据持久化）
- **真实天气**：查询城市实时天气并给出出行建议
- **Markdown 渲染**：支持代码高亮、表格、列表等格式

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

复制 `.env.example` 为 `.env`，填入你的 Kimi API Key：

```bash
cp .env.example .env
```

在 `.env` 中设置：

```
KIMI_API_KEY=sk-your-api-key-here
```

API Key 获取地址：https://platform.moonshot.cn （注册即送免费额度）

### 3. 启动服务

```bash
cd agent
python app.py
```

打开浏览器访问 http://localhost:5000

## 技术架构

```
┌──────────────────────────────────────┐
│       前端 (HTML/CSS/JS)              │
│   流式渲染 · Markdown · 思维链可视化   │
├──────────────────────────────────────┤
│       后端服务 (Flask)                │
│   SSE 流式接口 · REST API            │
├──────────────────────────────────────┤
│       智能体核心 (Agent)              │
│   Kimi API · Function Calling        │
├────────┬────────┬────────┬───────────┤
│ 对话记忆 │ 任务管理 │ 天气工具 │ 配置管理 │
└────────┴────────┴────────┴───────────┘
```

## 项目结构

```
ai-agent-homework/
├── agent/
│   ├── __init__.py       # 包导出
│   ├── agent.py          # 核心 Agent（Kimi API + Function Calling）
│   ├── config.py         # 配置管理
│   ├── memory.py         # 对话记忆
│   ├── tools.py          # 工具模块（任务 + 天气）
│   └── app.py            # Flask Web 服务
├── data/                  # 运行时数据（自动创建）
├── frontend/
│   └── index.html         # 前端界面
├── .env.example           # 环境变量模板
├── .gitignore
├── requirements.txt       # Python 依赖
└── README.md
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 大语言模型 | Kimi (Moonshot AI) moonshot-v1-8k |
| API 协议 | OpenAI 兼容格式 + Function Calling |
| 后端框架 | Flask |
| 前端 | HTML + CSS + JavaScript（原生） |
| 天气数据 | wttr.in 免费 API |
| Markdown | marked.js + highlight.js |

## 使用示例

- "帮我制定一个高数复习计划"
- "添加一个任务：明天交软工作业"
- "查看我的所有任务"
- "今天北京天气怎么样，适合出门吗？"
- "帮我完成任务 1 和 2"

## 团队成员

| 成员 | 学号 | 分工 |
|------|------|------|
| [姓名1] | [学号1] | 智能体核心逻辑、Kimi API 接入 |
| [姓名2] | [学号2] | 前端界面设计、流式渲染 |
| [姓名3] | [学号3] | 测试用例、项目文档 |
| [姓名4] | [学号4] | 工具模块、部署上线 |

## 许可证

MIT License
