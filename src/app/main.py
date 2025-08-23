from fastapi import FastAPI
from pydantic import BaseModel
from .services.infobip_service import InfobipService
from .services.chat_service import process_chat_message


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

    # Process chat message (5 steps: create chat, get user type, process message type, store message)
    chat_data = process_chat_message(message_data)
    
    # Extract processed data
    user_type = chat_data["user_type"]
    latest_message = chat_data["latest_message"]
    conversation_history = chat_data["conversation_history"]

    print(f"User type: {user_type}")    
    print(f"Latest message {latest_message}")

    print(f"Conversation: {conversation_history}")
    
    # # Get agent
    # agent = AgentFactory.get_agent(user_type)
    # # Process message with complete conversation context
    # agent_context = {
    #     "latest_message": latest_message,
    #     "conversation_history": conversation_history
    # }
    # agent_response = agent.process(agent_context)
    # # Send response to Infobip
    agent_response = {
        "message": "https://heysocialgeek.com/wp-content/uploads/2017/07/Bots-para-ganar-seguidores-likes-o-vistas-en-redes-sociales-1600x900.jpg",
        "type": "text"
    }
    infobip_service.send_message(message_data.get("from"), agent_response)

    return MessageResponse(
        message=agent_response.get("message"),
        status="success"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
