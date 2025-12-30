# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
from .chat import generate_response, check_ollama_status
from .db import init_db, list_conversations, get_conversation, delete_conversation, create_conversation

app = FastAPI(title="Alter Lab", description="AI Chat Interface with Persistent Conversations")

# Initialize DB on startup
init_db()

class UserMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
def root():
    """Serve the main chat interface"""
    import os
    html_path = os.path.join(os.path.dirname(__file__), 'static', 'index.html')
    with open(html_path, 'r') as f:
        return f.read()

@app.get("/ping")
def ping():
    return {"status": "pong", "who": "Alter Lab"}

@app.post("/chat")
def chat(user: UserMessage):
    """Send a message and get AI response"""
    # Create new conversation if none provided
    if not user.conversation_id:
        conversation_id = create_conversation()
    else:
        conversation_id = user.conversation_id
    
    try:
        response = generate_response(user.message, conversation_id)
        return {
            "response": response,
            "conversation_id": conversation_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations")
def get_conversations():
    """List all conversations"""
    try:
        conversations = list_conversations()
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations/{conversation_id}")
def get_conversation_history(conversation_id: str):
    """Get history of a specific conversation"""
    try:
        messages = get_conversation(conversation_id)
        if not messages:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {
            "conversation_id": conversation_id,
            "messages": messages
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/conversations/{conversation_id}")
def remove_conversation(conversation_id: str):
    """Delete a conversation"""
    try:
        deleted = delete_conversation(conversation_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/conversations")
def new_conversation():
    """Create a new conversation"""
    try:
        conversation_id = create_conversation()
        return {"conversation_id": conversation_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Check API and AI model health"""
    ollama_status = check_ollama_status()
    return {
        "api": "online",
        "ollama": ollama_status
    }
