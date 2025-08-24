# Broky - Digital Real Estate Agent

**Broky** is an intelligent WhatsApp-based digital real estate agent (broker digital) that automates tedious tasks for property sellers and buyers through natural conversation.

## Features

- 🏠 **Property Information Capture**: Collects property details through natural WhatsApp conversations
- 📄 **Document Generation**: Automatically generates printable property listing documents
- 👥 **Buyer Management**: Manages interested buyers automatically
- 📅 **Visit Scheduling**: Schedules property visits seamlessly
- 💬 **Communication Facilitation**: Bridges communication between sellers and buyers
- 🎤 **Audio Support**: Transcribes audio messages using OpenAI Whisper
- 🖼️ **Image Analysis**: Analyzes property images for additional information

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB Atlas
- **Messaging**: Infobip (WhatsApp Business API)
- **AI**: OpenAI GPT, Whisper (speech recognition)
- **Server**: Uvicorn ASGI server

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- MongoDB Atlas account (connection string required)
- Infobip account for WhatsApp Business API

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ia-hackaton-broky
```

### 2. Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
MONGODB_URI=your_mongodb_connection_string_here
DATABASE_NAME=broky_db
ENVIRONMENT=development

# Additional configuration variables as needed
OPENAI_API_KEY=your_openai_api_key
INFOBIP_API_KEY=your_infobip_api_key
INFOBIP_BASE_URL=your_infobip_base_url
```

## Running the Application

### Option 1: Using run_server.py (Recommended for Development)

```bash
python run_server.py
```

### Option 2: Direct Uvicorn

```bash
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: From main.py

```bash
python src/app/main.py
```

The application will be available at:
- **API**: http://localhost:8000
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

- `GET /` - Health check endpoint
- `GET /test-mongo` - MongoDB connection test
- `POST /webhook` - Infobip WhatsApp webhook endpoint

## Project Structure

```
src/app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration settings
├── api/                 # API endpoints and routing
├── core/                # Core business logic
│   ├── agent/          # AI agent implementations
│   │   ├── buyer/      # Buyer-specific agents
│   │   └── seller/     # Seller-specific agents
│   ├── crud/           # Database CRUD operations
│   ├── tools/          # AI agent tools
│   └── database.py     # MongoDB connection
├── models/             # Pydantic models and MongoDB schemas
├── services/           # External service integrations
│   ├── infobip_service.py    # WhatsApp messaging
│   ├── chat_service.py       # Chat management
│   └── image_integration_service.py  # Image processing
└── utils/              # Utility functions
    ├── logger.py       # Logging configuration
    ├── openai.py       # OpenAI integrations
    └── whatsapp_qr.py  # QR code generation
```

## Development

### MongoDB Operations

Test MongoDB connection:
```bash
python test_mongo.py
```

Query database using scripts:
```bash
# List collections
python scripts/mongo_query.py list

# Query documents
python scripts/mongo_query.py query -c [collection]
python scripts/mongo_query.py query -c [collection] -f '{"field": "value"}'

# Insert document
python scripts/mongo_query.py insert -c [collection] -d '{"key": "value"}'
```

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
7. **Database Update**: All interactions stored in MongoDB
8. **Message Delivery**: Response sent back via Infobip

## Deployment

### Railway Deployment

```bash
# Login and link project
railway login
railway link -p PROJECT_NAME

# Set environment variables
railway variables --set "MONGODB_URI=your_connection_string"
railway variables --set "DATABASE_NAME=broky_db"
railway variables --set "ENVIRONMENT=production"

# Deploy
railway up

# Check status and get URL
railway status
railway domain
```

### Docker Support

The project includes `Dockerfile` and `docker-compose.yml` for containerized deployment.

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For support and questions, please refer to the project documentation or open an issue in the repository