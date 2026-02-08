from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from .database import engine, init_db, get_session
from .models import Conversation, Message, Task
from .agent import run_agent
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

app = FastAPI(title="AI Todo Chatbot")

@app.on_event("startup")
def on_startup():
    init_db()

class ChatRequest(BaseModel):
    conversation_id: Optional[UUID] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: UUID
    response: str

@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(user_id: str, request: ChatRequest, session: Session = Depends(get_session)):
    # 1. Get or create conversation
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # 2. Store user message
    user_msg = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message
    )
    session.add(user_msg)
    
    # 3. Build message history for agent
    history_statement = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at)
    history_messages = session.exec(history_statement).all()
    
    agent_messages = [
        {"role": msg.role, "content": msg.content}
        for msg in history_messages
    ]
    
    # 4. Run agent
    try:
        agent_response_content = await run_agent(agent_messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 5. Store assistant response
    assistant_msg = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=agent_response_content
    )
    session.add(assistant_msg)
    session.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=agent_response_content
    )

@app.get("/api/{user_id}/tasks")
async def get_user_tasks(user_id: str, session: Session = Depends(get_session)):
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks
