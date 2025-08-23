from fastapi import FastAPI
from pydantic import BaseModel

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
    return {"message": "Welcome to IA Hackaton Broky API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)