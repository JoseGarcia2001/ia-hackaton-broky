#!/bin/bash
# Quick MongoDB shell connection script

# Load environment variables
source .env

# Connect to MongoDB Atlas using mongosh
echo "🔗 Connecting to MongoDB Atlas..."
echo "📊 Database: $DATABASE_NAME"
echo ""

# Check if mongosh is installed
if ! command -v mongosh &> /dev/null; then
    echo "⚠️  mongosh not found. Install it with:"
    echo "    brew install mongodb-community-shell"
    echo "    or download from: https://www.mongodb.com/try/download/shell"
    exit 1
fi

# Connect with mongosh
mongosh "$MONGODB_URI/$DATABASE_NAME"