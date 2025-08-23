from fastapi import FastAPI
from pydantic import BaseModel
from .services.infobip_service import InfobipService


app = FastAPI(
    title="IA Hackaton Broky API",
    description="API desarrollada para el hackaton con FastAPI",
    version="1.0.0"
)

class MessageResponse(BaseModel):
    message: str
    status: str


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


@app.get("/")
async def root():
    return {"status": "healthy", "message": "Broky API is running", "version": "1.0.0"}

# Webhook endpoint for Infobip
@app.post("/webhook")
async def infobip_webhook(webhook_data: dict):
    # recibir mensaje de infobip este es el webhook
    infobip_service = InfobipService()
    # Receive message from Infobip
    message_data = infobip_service.receive_webhook_message(webhook_data)
    # # Create chat
    # chat = Chat()
    # # Get user type
    # user_type = chat.get_user_type(message_data)
    # # Process message type
    # processed_message_type = infobip_service.process_message_type(message_data)
    # # Add message to MongoDB
    # chat.add_message_mongo(processed_message_type)
    # # Get agent
    # agent = AgentFactory.get_agent(user_type)
    # # Process message
    # agent_response = agent.process(processed_message_type)
    # # Send response to Infobip
    agent_response = "Hola, ¿cómo estás?"
    print(agent_response)
    infobip_service.send_text_message(message_data.get("from"), agent_response)

    # chat.add_message_mongo(agent_response)

    return MessageResponse(
        message=agent_response,
        status="success"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)