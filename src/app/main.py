from fastapi import FastAPI
from pydantic import BaseModel
from .services.infobip_service import InfobipService
from .services.chat_service import process_chat_message, save_agent_response
from .core.agents_factory import AgentsFactory


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
    chat_id = chat_data["chat_id"]

    print(f"User type: {user_type}")    
    print(f"Latest message {latest_message}")

    print(f"Conversation: {conversation_history}")
    
    # Get agent
    context = {"chat_id": chat_id}
    # agent = AgentsFactory.get_agent(user_type, context)
    # print(f"Using agent: {agent.__class__.__name__}")

    # # Process message with complete conversation context
    # agent_context = {
    #     "latest_message": latest_message,
    #     "conversation_history": conversation_history,
    #     "chat_id": chat_id
    # }
    # agent_response = agent.process(agent_context)
    # # Send response to Infobip
    agent_response = {
        "message": "Gracias por tu mensaje, en breve te responderemos",
        "type": "text"
    }
    infobip_service.send_message(message_data.get("from"), agent_response)
    
    # Save agent response to chat history
    save_agent_response(chat_id, agent_response["message"])

    return MessageResponse(
        message=agent_response.get("message"),
        status="success"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
