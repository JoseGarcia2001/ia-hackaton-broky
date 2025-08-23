from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

# Simple connection
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "broky_db")

def get_db():
    """Get database connection"""
    client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
    return client[DATABASE_NAME]

def test_connection():
    """Test MongoDB connection"""
    try:
        client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
        client.admin.command('ping')
        print("✅ Connected to MongoDB!")
        
        # Insert a test document
        db = client[DATABASE_NAME]
        test_collection = db.test
        result = test_collection.insert_one({"test": "Hello MongoDB!", "timestamp": "now"})
        print(f"📝 Test document inserted with id: {result.inserted_id}")
        
        client.close()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False