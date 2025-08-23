#!/usr/bin/env python3
"""
MongoDB Query Helper
Usage: python scripts/mongo_query.py
"""
import os
import sys
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import json
from bson import ObjectId

load_dotenv()

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def connect():
    uri = os.getenv("MONGODB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client[os.getenv("DATABASE_NAME", "broky_db")]

def query(collection_name, filter_dict=None, limit=10):
    """Query a collection"""
    db = connect()
    collection = db[collection_name]
    cursor = collection.find(filter_dict or {}).limit(limit)
    results = list(cursor)
    print(json.dumps(results, indent=2, cls=JSONEncoder))
    return results

def insert(collection_name, document):
    """Insert a document"""
    db = connect()
    collection = db[collection_name]
    result = collection.insert_one(document)
    print(f"Inserted with ID: {result.inserted_id}")
    return result.inserted_id

def list_collections():
    """List all collections"""
    db = connect()
    collections = db.list_collection_names()
    print("Collections:", collections)
    return collections

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='MongoDB Query Tool')
    parser.add_argument('action', choices=['query', 'insert', 'list'], help='Action to perform')
    parser.add_argument('-c', '--collection', help='Collection name')
    parser.add_argument('-f', '--filter', help='Filter as JSON string', default='{}')
    parser.add_argument('-d', '--document', help='Document to insert as JSON string')
    parser.add_argument('-l', '--limit', type=int, default=10, help='Limit results')
    
    args = parser.parse_args()
    
    if args.action == 'list':
        list_collections()
    elif args.action == 'query':
        if not args.collection:
            print("Error: Collection name required for query")
            sys.exit(1)
        filter_dict = json.loads(args.filter)
        query(args.collection, filter_dict, args.limit)
    elif args.action == 'insert':
        if not args.collection or not args.document:
            print("Error: Collection name and document required for insert")
            sys.exit(1)
        doc = json.loads(args.document)
        insert(args.collection, doc)