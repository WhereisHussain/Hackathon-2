# Project Specification: AI-Powered Todo Chatbot with MCP

## Overview
An AI-powered todo management chatbot using a stateless FastAPI backend, OpenAI Agents SDK, and MCP (Model Context Protocol) for task operations. The frontend will use OpenAI ChatKit for a conversational UI.

## Requirements

### Functional Requirements
- **Task Management**: Create, list, update, complete, and delete tasks via natural language.
- **Conversational AI**: Utilize OpenAI Agents SDK to process natural language and call MCP tools.
- **Stateless Backend**: The FastAPI server will not hold session/conversation state in memory. All state (tasks, conversations, messages) will be persisted in a Neon PostgreSQL database.
- **MCP Integration**: An MCP server will expose task CRUD operations as tools for the AI agent.
- **Authentication**: User authentication using Better Auth (likely integrated on the frontend).
- **History Persistence**: Conversations and messages will be stored in the database and retrieved on each request to provide context.

### Technical Stack
- **Frontend**: Next.js with OpenAI ChatKit.
- **Backend**: Python FastAPI.
- **AI**: OpenAI Agents SDK (Python).
- **MCP**: Official MCP SDK (Python).
- **ORM**: SQLModel.
- **Database**: Neon Serverless PostgreSQL.
- **Auth**: Better Auth.

## Database Schema (SQLModel)

### Task
- `id`: uuid (primary key)
- `user_id`: string
- `title`: string
- `description`: string (optional)
- `completed`: boolean (default: false)
- `created_at`: datetime
- `updated_at`: datetime

### Conversation
- `id`: uuid (primary key)
- `user_id`: string
- `created_at`: datetime
- `updated_at`: datetime

### Message
- `id`: uuid (primary key)
- `conversation_id`: uuid (foreign key)
- `user_id`: string
- `role`: string (user/assistant)
- `content`: string
- `created_at`: datetime

## API Endpoints

### Chat Endpoint
- `POST /api/{user_id}/chat`
  - Body: `{ "conversation_id": "...", "message": "..." }`
  - Logic:
    1. Fetch conversation history.
    2. Initialize OpenAI Agent with history.
    3. Agent calls MCP tools as needed.
    4. Store user and assistant messages in DB.
    5. Return response and tool call info.

## MCP Tools
- `add_task(user_id, title, description)`
- `list_tasks(user_id, status)`
- `complete_task(user_id, task_id)`
- `delete_task(user_id, task_id)`
- `update_task(user_id, task_id, title, description)`

## Implementation Strategy
1. **Specs**: Document requirements and design (this file).
2. **Plan**: Define the development steps.
3. **Execution**:
   - Initialize project structure.
   - Setup DB models and migrations.
   - Implement MCP Server.
   - Implement Agent Runner and Chat Endpoint.
   - Build ChatKit-based frontend.
4. **Verification**: Manual and automated testing of the chat flow.
