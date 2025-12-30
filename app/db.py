# app/db.py
import sqlite3
import uuid
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = "memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Drop old table if it exists (for migration)
    cursor.execute('DROP TABLE IF EXISTS conversations')
    
    # Create new schema with conversation_id and timestamps
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversation_metadata(conversation_id)
        )
    ''')
    
    # Create metadata table for conversations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation_metadata (
            conversation_id TEXT PRIMARY KEY,
            title TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def create_conversation() -> str:
    """Create a new conversation and return its ID"""
    conversation_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversation_metadata (conversation_id, title, created_at, updated_at)
        VALUES (?, ?, ?, ?)
    ''', (conversation_id, "New Conversation", timestamp, timestamp))
    conn.commit()
    conn.close()
    
    return conversation_id

def save_conversation(conversation_id: str, user_msg: str, bot_msg: str):
    """Save a message exchange to a conversation"""
    timestamp = datetime.now().isoformat()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if conversation exists, create if not
    cursor.execute('SELECT conversation_id FROM conversation_metadata WHERE conversation_id = ?', (conversation_id,))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO conversation_metadata (conversation_id, title, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (conversation_id, "New Conversation", timestamp, timestamp))
    
    # Save the message
    cursor.execute('''
        INSERT INTO conversations (conversation_id, user_message, bot_response, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (conversation_id, user_msg, bot_msg, timestamp))
    
    # Update conversation metadata
    cursor.execute('''
        UPDATE conversation_metadata 
        SET updated_at = ?,
            title = CASE 
                WHEN title = 'New Conversation' THEN substr(?, 1, 50)
                ELSE title
            END
        WHERE conversation_id = ?
    ''', (timestamp, user_msg, conversation_id))
    
    conn.commit()
    conn.close()

def get_conversation(conversation_id: str) -> List[Dict]:
    """Get all messages in a conversation"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_message, bot_response, timestamp
        FROM conversations
        WHERE conversation_id = ?
        ORDER BY id ASC
    ''', (conversation_id,))
    
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return messages

def list_conversations() -> List[Dict]:
    """List all conversations with metadata"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            cm.conversation_id,
            cm.title,
            cm.created_at,
            cm.updated_at,
            COUNT(c.id) as message_count
        FROM conversation_metadata cm
        LEFT JOIN conversations c ON cm.conversation_id = c.conversation_id
        GROUP BY cm.conversation_id
        ORDER BY cm.updated_at DESC
    ''')
    
    conversations = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return conversations

def delete_conversation(conversation_id: str) -> bool:
    """Delete a conversation and all its messages"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM conversations WHERE conversation_id = ?', (conversation_id,))
    cursor.execute('DELETE FROM conversation_metadata WHERE conversation_id = ?', (conversation_id,))
    
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return deleted
