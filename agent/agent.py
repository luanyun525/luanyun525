"""AI 学习伴侣 - 核心智能体模块"""

import json
import logging
from typing import Generator

from openai import OpenAI

from .config import KIMI_API_KEY, KIMI_BASE_URL, KIMI_MODEL, SYSTEM_PROMPT, MAX_HISTORY
from .memory import ConversationMemory
from .tools import TaskManager, WeatherTool

logger = logging.getLogger(__name__)


class SmartAssistant:
    """基于 LLM API 的智能学习助手（兼容 OpenAI 格式）"""

    # Function Calling 工具定义
    TOOLS_SCHEMA = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "添加一个新的待办任务",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "任务标题"},
                        "description": {"type": "string", "description": "任务描述（可选）"},
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "优先级（默认 medium）",
                        },
                    },
                    "required": ["title"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "获取用户的待办任务列表",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["pending", "completed"],
                            "description": "按状态筛选任务（可选，不填则返回全部）",
                        }
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "将指定任务标记为已完成",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "任务 ID"}
                    },
                    "required": ["task_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "删除指定的任务",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "任务 ID"}
                    },
                    "required": ["task_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "查询指定城市的实时天气信息，给出穿衣和出行建议",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称（支持中文，如'北京'、'上海'）",
                        }
                    },
                    "required": ["city"],
                },
            },
        },
    ]

    def __init__(self, api_key: str = None):
        api_key = api_key or KIMI_API_KEY
        if not api_key:
            raise ValueError(
                "未配置 KIMI_API_KEY。请在 .env 文件中设置，或传入 api_key 参数。"
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url=KIMI_BASE_URL,
        )
        self.model = KIMI_MODEL
        self.memory = ConversationMemory(max_history=MAX_HISTORY)
        self.task_manager = TaskManager()
        self.weather_tool = WeatherTool()
        self._supports_tools = None  # 延迟检测模型是否支持 function calling

    def _check_tool_support(self) -> bool:
        """检测当前模型是否支持 function calling（tools 参数）"""
        if self._supports_tools is not None:
            return self._supports_tools
        try:
            # 尝试带 tools 参数调用，如果失败则标记为不支持
            test_messages = [
                {"role": "system", "content": "你是一个助手。"},
                {"role": "user", "content": "你好"},
            ]
            self.client.chat.completions.create(
                model=self.model,
                messages=test_messages,
                tools=self.TOOLS_SCHEMA,
                max_tokens=5,
            )
            self._supports_tools = True
        except Exception:
            logger.info("当前模型不支持 function calling，将使用纯对话模式")
            self._supports_tools = False
        return self._supports_tools

    def _call_api(self, messages: list, tools=None, stream=False, temperature=0.7):
        """统一的 API 调用方法，自动处理 tools 兼容性"""
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
        }
        # 仅在模型支持时传入 tools
        if tools and self._check_tool_support():
            kwargs["tools"] = tools
        return self.client.chat.completions.create(**kwargs)

    def process(self, user_input: str) -> dict:
        """处理用户输入，返回完整响应（非流式）"""
        self.memory.add_message("user", user_input)
        messages = self._build_messages()

        try:
            response = self._call_api(messages, tools=self.TOOLS_SCHEMA)
        except Exception as e:
            logger.error("API 调用失败: %s", e)
            fallback = "抱歉，AI 服务暂时不可用，请稍后再试。"
            self.memory.add_message("assistant", fallback)
            return {"success": False, "action": "error", "message": fallback}

        # 兼容处理：某些模型可能返回字符串而非标准对象
        resp_data = response
        if isinstance(response, str):
            self.memory.add_message("assistant", response)
            return {"success": True, "action": "chat", "message": response}

        try:
            message = resp_data.choices[0].message
        except (AttributeError, IndexError, TypeError):
            # 非标准响应格式，直接作为文本处理
            text = str(resp_data) if resp_data else "收到"
            self.memory.add_message("assistant", text)
            return {"success": True, "action": "chat", "message": text}

        # 处理工具调用
        if hasattr(message, 'tool_calls') and message.tool_calls:
            reply = self._handle_tool_calls(message, messages)
        else:
            reply = message.content or ""

        self.memory.add_message("assistant", reply)
        return {"success": True, "action": "chat", "message": reply}

    def process_stream(self, user_input: str) -> Generator[str, None, None]:
        """处理用户输入，流式返回文本片段"""
        self.memory.add_message("user", user_input)
        messages = self._build_messages()

        try:
            first_response = self._call_api(messages, tools=self.TOOLS_SCHEMA)
        except Exception as e:
            logger.error("API 调用失败: %s", e)
            error_msg = "抱歉，AI 服务暂时不可用，请稍后再试。"
            self.memory.add_message("assistant", error_msg)
            yield error_msg
            return

        # 兼容非标准响应
        if isinstance(first_response, str):
            self.memory.add_message("assistant", first_response)
            yield first_response
            return

        try:
            first_message = first_response.choices[0].message
        except (AttributeError, IndexError, TypeError):
            text = str(first_response) if first_response else ""
            self.memory.add_message("assistant", text)
            yield text
            return

        if hasattr(first_message, 'tool_calls') and first_message.tool_calls:
            # 有工具调用：执行工具，然后流式输出最终回复
            result_text = self._handle_tool_calls(first_message, messages)
            messages.append(first_message)
            for tc in first_message.tool_calls:
                tool_result = self._get_tool_result(tc)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": tool_result,
                    }
                )
            messages.append({"role": "assistant", "content": result_text})

            # 流式输出
            full_reply = ""
            try:
                stream = self._call_api(messages, stream=True)
                for chunk in stream:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        full_reply += delta.content
                        yield delta.content
            except Exception:
                full_reply = result_text
                yield result_text

            self.memory.add_message("assistant", full_reply)
        else:
            # 无工具调用：直接流式输出
            full_reply = ""
            try:
                stream = self._call_api(messages, stream=True)
                for chunk in stream:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        full_reply += delta.content
                        yield delta.content
            except Exception as e:
                logger.error("流式输出失败: %s", e)
                full_reply = first_message.content or ""
                yield full_reply

            self.memory.add_message("assistant", full_reply)

    def _build_messages(self) -> list:
        """构建发送给 Kimi API 的 messages 数组"""
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in self.memory.get_openai_messages():
            messages.append(msg)
        return messages

    def _handle_tool_calls(self, message, messages: list) -> str:
        """处理工具调用，返回最终文本回复"""
        # 将助手消息（含 tool_calls）加入上下文
        messages.append(message)

        for tool_call in message.tool_calls:
            result_str = self._get_tool_result(tool_call)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result_str,
                }
            )

        # 再次调用 API 获取最终回复
        try:
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
            )
            return final_response.choices[0].message.content or ""
        except Exception as e:
            logger.error("获取工具调用最终回复失败: %s", e)
            return "工具调用已完成，但生成回复时出错。"

    def _get_tool_result(self, tool_call) -> str:
        """执行单个工具调用，返回 JSON 字符串"""
        func_name = tool_call.function.name
        try:
            arguments = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
            return json.dumps({"error": "参数解析失败"}, ensure_ascii=False)

        result = self._execute_tool(func_name, arguments)
        return json.dumps(result, ensure_ascii=False, default=str)

    def _execute_tool(self, tool_name: str, arguments: dict):
        """根据工具名称执行对应函数"""
        if tool_name == "add_task":
            return self.task_manager.add_task(
                title=arguments.get("title", ""),
                description=arguments.get("description", ""),
                priority=arguments.get("priority", "medium"),
            )
        elif tool_name == "list_tasks":
            return self.task_manager.list_tasks(
                status=arguments.get("status")
            )
        elif tool_name == "complete_task":
            return self.task_manager.complete_task(
                task_id=arguments.get("task_id")
            )
        elif tool_name == "delete_task":
            return self.task_manager.delete_task(
                task_id=arguments.get("task_id")
            )
        elif tool_name == "get_weather":
            return self.weather_tool.get_weather(
                city=arguments.get("city", "")
            )
        else:
            return {"error": f"未知工具: {tool_name}"}

    def get_history(self):
        """获取对话历史"""
        return self.memory.get_history()
