# Alter Lab - AI Chat Interface

> Real-time AI chat interface with persistent conversation history and embeddings

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)](https://fastapi.tiangolo.com/)
[![Status](https://img.shields.io/badge/Status-Active%20Development-yellow)](https://github.com)

[**🎬 Screenshot Coming Soon**]

## Features

- 💬 **Real-time AI Chat** - Interactive conversational AI interface
- 🗄️ **Persistent Conversations** - SQLite-based conversation storage
- 🔍 **Semantic Search** - Text embeddings for intelligent conversation retrieval
- 🚀 **FastAPI Backend** - High-performance async API
- 🎨 **Modern Web UI** - Clean, responsive chat interface
- 📊 **RESTful API** - Full API access for custom integrations
- 🔐 **Session Management** - Multi-conversation support

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   cd /path/to/alter-lab
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Open in browser:**
   ```
   http://localhost:8000
   ```

That's it! Start chatting with the AI.

## Usage

### Web Interface

1. Navigate to `http://localhost:8000`
2. Type your message in the chat box
3. Press Enter or click Send
4. View conversation history in the sidebar

### API Endpoints

#### **POST /chat** - Send a message
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

Response:
```json
{
  "response": "I'm doing well, thank you!",
  "conversation_id": "abc123"
}
```

#### **GET /conversations** - List all conversations
```bash
curl "http://localhost:8000/conversations"
```

#### **GET /conversations/{id}** - Get specific conversation
```bash
curl "http://localhost:8000/conversations/abc123"
```

#### **DELETE /conversations/{id}** - Delete conversation
```bash
curl -X DELETE "http://localhost:8000/conversations/abc123"
```

#### **GET /docs** - Interactive API documentation
```
http://localhost:8000/docs
```

## Architecture

```
alter-lab/
├── app/
│   ├── main.py           # FastAPI application & web UI
│   ├── chat.py           # Chat logic & AI integration
│   ├── db.py             # Database operations
│   └── embeddings.py     # Text embeddings & semantic search
├── memory.db             # SQLite database
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite
- **AI Integration:** Configurable (Ollama/OpenAI/HuggingFace)
- **Embeddings:** Sentence Transformers
- **Frontend:** Vanilla JavaScript + HTML/CSS

## Configuration

### AI Model

Edit `app/chat.py` to configure your AI model:

```python
# Option 1: Use Ollama (local, free)
# Requires: brew install ollama && ollama pull llama2

# Option 2: Use OpenAI (API key required)
# Set environment variable: export OPENAI_API_KEY=your_key

# Option 3: Use HuggingFace Transformers (local)
# Automatically downloads models on first run
```

### Database

The application uses SQLite by default. The database file `memory.db` is created automatically on first run.

To reset the database:
```bash
rm memory.db
# Restart the server
```

## Development

### Run in development mode:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Run tests:
```bash
pytest tests/
```

### View logs:
```bash
tail -f server.log
```

## Deployment

### Docker (Coming Soon)
```bash
docker build -t alter-lab .
docker run -p 8000:8000 alter-lab
```

### Cloud Deployment
Deploy to Railway, Render, or Fly.io:
1. Push code to GitHub
2. Connect repository to platform
3. Set environment variables (if using OpenAI)
4. Deploy

**Live Demo:** Coming Soon

## Roadmap

- [x] Basic chat functionality
- [x] Conversation persistence
- [x] RESTful API
- [ ] Real AI model integration
- [ ] Conversation history UI
- [ ] Semantic search
- [ ] User authentication
- [ ] Multi-user support
- [ ] Export conversations
- [ ] Dark mode

## Screenshots

### Chat Interface
[**Coming Soon**]

### API Documentation
[**Coming Soon**]

## Troubleshooting

**Server won't start:**
```bash
# Check if port 8000 is already in use
lsof -i :8000
# Kill the process if needed
kill -9 <PID>
```

**Database errors:**
```bash
# Reset database
rm memory.db
# Restart server
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Contributing

Contributions welcome! Areas needing work:
- AI model integration improvements
- UI/UX enhancements
- Additional API endpoints
- Documentation improvements

## License

MIT License - Feel free to use and modify!

## Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SQLite](https://www.sqlite.org/) - Lightweight database
- [Sentence Transformers](https://www.sbert.net/) - Text embeddings
