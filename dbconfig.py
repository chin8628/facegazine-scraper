from typing import Collection, OrderedDict
from pymongo import MongoClient


def create_db():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)

    return client.facegazine


def setup_collection(db):
    db.posts
    db.pages

    vexpr = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["post_id", "updated_at", "created_at"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "must be a string and is required",
                },
                "updated_at": {
                    "bsonType": "date",
                    "description": "must be a date and is required",
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "must be a date and is required",
                },
            },
        }
    }

    cmd = OrderedDict(
        [("collMod", "posts"), ("validator", vexpr), ("validationLevel", "moderate")]
    )

    db.command(cmd)

    return db
