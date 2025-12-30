# app/chat.py
import requests
import os
from typing import List, Dict
from .db import save_conversation, get_conversation
from .embeddings import embed_text

OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2:1b"  # Fast, small model

def check_ollama_status() -> Dict:
    """Check if Ollama is running and available"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return {"status": "online", "models": [m['name'] for m in models]}
    except:
        pass
    return {"status": "offline", "models": []}

def generate_response(user_message: str, conversation_id: str) -> str:
    """
    Generate AI response using Ollama with conversation context.
    Falls back to OpenAI if Ollama is unavailable.
    """
    
    # Get conversation history for context
    history = get_conversation(conversation_id)
    
    # Build messages with context
    messages = [{"role": "system", "content": "You are Alter, a helpful and friendly AI assistant."}]
    
    # Add conversation history (last 10 messages for context)
    for msg in history[-10:]:
        messages.append({"role": "user", "content": msg['user_message']})
        messages.append({"role": "assistant", "content": msg['bot_response']})
    
    # Add current message
    messages.append({"role": "user", "content": user_message})
    
    # Try Ollama first
    try:
        bot_message = _call_ollama(messages)
    except Exception as e:
        # Fallback to OpenAI if available
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            try:
                bot_message = _call_openai(messages, openai_key)
            except Exception as e2:
                bot_message = f"Sorry, I'm having trouble connecting to my AI brain. Error: {str(e)}"
        else:
            bot_message = f"Sorry, I'm having trouble connecting to Ollama. Please make sure it's running (brew services start ollama). Error: {str(e)}"
    
    # Save to memory
    save_conversation(conversation_id, user_message, bot_message)
    
    # Generate embedding (optional - for future semantic search)
    try:
        _ = embed_text(user_message)
    except:
        pass
    
    return bot_message

def _call_ollama(messages: List[Dict]) -> str:
    """Call Ollama API for response"""
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    }
    
    response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    return result['message']['content']

def _call_openai(messages: List[Dict], api_key: str) -> str:
    """Call OpenAI API as fallback"""
    import openai
    openai.api_key = api_key
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content
