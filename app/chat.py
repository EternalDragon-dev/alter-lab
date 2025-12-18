# app/chat.py
from .db import save_conversation
from .embeddings import embed_text

def generate_response(user_message):
    # For now, echo with a little Omega flavor
    bot_message = f"Ooooh, I got your message: '{user_message}'"
    
    # Save to memory
    save_conversation(user_message, bot_message)
    
    # Generate embedding (stub)
    _ = embed_text(user_message)
    
    return bot_message
