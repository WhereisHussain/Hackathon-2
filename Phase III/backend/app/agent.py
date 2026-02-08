import os
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from typing import List, Optional
from .mcp_server import add_task, list_tasks, complete_task, delete_task, update_task
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AGENT_INSTRUCTIONS = """
You are a helpful Todo Assistant. Your goal is to help users manage their tasks using the provided tools.
You can add, list, complete, delete, and update tasks.
Always confirm actions with a friendly response.
If a user asks for something you can't do, explain your capabilities.
When listing tasks, present them clearly to the user.
Wait for tool outputs before responding to the user about the result of an action.
"""

# Mapping MCP tools to OpenAI tool definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Retrieve tasks from the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as complete",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "string"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Remove a task from the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "string"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Modify task title or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    }
]

async def run_agent(messages: List[ChatCompletionMessageParam]) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": AGENT_INSTRUCTIONS}] + messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message
    
    if assistant_message.tool_calls:
        messages.append(assistant_message)
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            # Call corresponding MCP tool
            if function_name == "add_task":
                result = await add_task(**args)
            elif function_name == "list_tasks":
                result = await list_tasks(**args)
            elif function_name == "complete_task":
                result = await complete_task(**args)
            elif function_name == "delete_task":
                result = await delete_task(**args)
            elif function_name == "update_task":
                result = await update_task(**args)
            else:
                result = json.dumps({"error": "Tool not found"})
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": result
            })
        
        # Get final response from agent after tool calls
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": AGENT_INSTRUCTIONS}] + messages
        )
        return final_response.choices[0].message.content
    
    return assistant_message.content
