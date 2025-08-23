# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Broky** is a digital real estate agent (broker digital) that automates tedious tasks for property sellers and buyers. It's an intelligent WhatsApp-based assistant that:
- Captures property information through natural conversation
- Generates printable documents for property listings
- Manages interested buyers automatically
- Schedules property visits
- Facilitates communication between sellers and buyers

## Architecture Overview

### Technology Stack
- **Backend Framework**: FastAPI (Python)
- **Database**: MongoDB (planned)
- **Messaging Platform**: Infobip (WhatsApp Business API)
- **Speech Recognition**: OpenAI Whisper (for audio transcription)
- **Server**: Uvicorn ASGI server

### System Flow
1. **User Interaction**: Users interact via WhatsApp through Infobip
2. **User Classification**: System identifies if user is seller (registered) or buyer (new)
3. **Message Processing**:
   - Audio messages → Transcribed with Whisper
   - Images → Analyzed for property information
   - Text → Direct processing
4. **Intent Recognition**: System determines user intent
5. **Agent Processing**: AI agent handles the request based on intent
6. **Response Generation**: Agent generates appropriate response
7. **Database Update**: All interactions are stored in MongoDB
8. **Message Delivery**: Response sent back via Infobip

### Project Structure
```
src/app/
├── main.py          # FastAPI application entry point
├── api/             # API endpoints (webhooks for Infobip, etc.)
├── core/            # Core business logic
├── models/          # Pydantic models and MongoDB schemas
├── services/        # External service integrations (Infobip, Whisper, AI agent)
└── utils/           # Utility functions
```

## Development Commands

### Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Run Development Server
```bash
# Option 1: Using run_server.py (with auto-reload)
python run_server.py

# Option 2: Direct uvicorn
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000

# Option 3: From main.py
python src/app/main.py
```

### API Documentation
Once running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## MongoDB Setup
MongoDB Atlas is configured and ready to use. Connection is handled through `src/app/core/database.py`

### Quick MongoDB Usage
```python
from src.app.core.database import get_db

# Get database instance
db = get_db()

# Example: Insert document
collection = db['test']
result = collection.insert_one({"message": "Hello"})

# Example: Query documents
docs = collection.find({"status": "active"})
```

## Environment Variables
Copy `.env.example` to `.env` and configure:
```
MONGODB_URI=your_mongodb_connection_string_here
DATABASE_NAME=broky_db
ENVIRONMENT=development
```

## MongoDB Quick Access

### Test Connection
```bash
python test_mongo.py
```

### Query Database from Terminal
```bash
# List all collections
python scripts/mongo_query.py list

# Query documents
python scripts/mongo_query.py query -c test
python scripts/mongo_query.py query -c users -f '{"user_type": "seller"}'

# Insert document
python scripts/mongo_query.py insert -c test -d '{"name": "test", "value": 123}'

# Direct MongoDB Shell (if mongosh installed)
./scripts/mongo_shell.sh
```

### MongoDB Connection String
Database is already configured in `.env` file. Use the helper functions in `src/app/core/database.py`:
```python
from src.app.core.database import get_db
db = get_db()
```

## Next Implementation Steps
1. Set up Infobip webhook endpoint in `api/` directory
2. Create Whisper integration service
3. Build message processing pipeline
4. Implement AI agent logic for different intents
5. Add conversation state management