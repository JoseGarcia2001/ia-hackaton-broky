from fastapi import FastAPI
from pydantic import BaseModel
from app.services.infobip_service import InfobipService


app = FastAPI(
    title="IA Hackaton Broky API",
    description="API desarrollada para el hackaton con FastAPI",
    version="1.0.0"
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

# MongoDB test endpoint
@app.get("/test-mongo")
async def test_mongo():
    try:
        from .core.database import test_connection
        success = test_connection()
        if success:
            return {"status": "success", "message": "MongoDB connected successfully"}
        else:
            return {"status": "error", "message": "MongoDB connection failed"}
    except Exception as e:
        return {"status": "error", "message": f"MongoDB error: {str(e)}"}

class MessageResponse(BaseModel):
    message: str
    status: str

@app.post("/main", response_model=MessageResponse)
async def hello_world():
    return MessageResponse(
        message="Hello World from FastAPI!",
        status="success"
    )

@app.get("/")
async def root():
    # recibir mensaje de infobip este es el webhhok
    infobip_service = InfobipService()
    chat = Chat()
    # Receive message from Infobip
    message_data = infobip_service.receive_webhook_message()
    # Get user type
    user_type = chat.get_user_type(message_data)
    # Process message type
    processed_message_type = infobip_service.process_message_type(message_data)
    # Add message to MongoDB
    chat.add_message_mongo(processed_message_type)
    # Get agent
    agent = AgentFactory.get_agent(user_type)
    # Process message
    agent_response = agent.process(processed_message_type)
    # Send response to Infobip
    infobip_service.send_response(agent_response)

    chat.add_message_mongo(agent_response)

    return {"message": agent_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)