# app/main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from .chat import generate_response
from .db import init_db

app = FastAPI()

# Initialize DB on startup
init_db()

class UserMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Alter Lab Chat</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #333; }
            input {
                width: 70%;
                padding: 10px;
                font-size: 16px;
                border: 2px solid #ddd;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover { background: #0056b3; }
            #response {
                margin-top: 20px;
                padding: 15px;
                background: #e7f3ff;
                border-radius: 5px;
                display: none;
            }
            .links { margin-top: 20px; }
            .links a { margin-right: 15px; color: #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔮 Alter Lab Chat</h1>
            <p>Send a message to Alter:</p>
            <input type="text" id="message" placeholder="Type your message here..." />
            <button onclick="sendMessage()">Send</button>
            <div id="response"></div>
            <div class="links">
                <a href="/docs" target="_blank">📚 API Docs</a>
                <a href="/ping" target="_blank">🏓 Ping</a>
            </div>
        </div>
        <script>
            async function sendMessage() {
                const message = document.getElementById('message').value;
                const responseDiv = document.getElementById('response');
                
                if (!message) {
                    alert('Please enter a message!');
                    return;
                }
                
                responseDiv.style.display = 'block';
                responseDiv.innerHTML = '⏳ Sending...';
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    });
                    const data = await response.json();
                    responseDiv.innerHTML = '<strong>Alter:</strong> ' + data.response;
                } catch (error) {
                    responseDiv.innerHTML = '❌ Error: ' + error.message;
                }
            }
            
            document.getElementById('message').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    """

@app.get("/ping")
def ping():
    return {"status": "pong", "who": "Alter Lab"}

@app.post("/chat")
def chat(user: UserMessage):
    response = generate_response(user.message)
    return {"response": response}
