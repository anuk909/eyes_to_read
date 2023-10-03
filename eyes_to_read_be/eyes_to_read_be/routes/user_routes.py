# user_routes.py

from fastapi import APIRouter, HTTPException, Body
from pymongo import MongoClient
from eyes_to_read_be.common.config import MONGO_URI
from eyes_to_read_be.common.models import User
import uuid

user_router = APIRouter(prefix="/users")

client = MongoClient(MONGO_URI)
db = client["eyes_to_see_db"]
users_collection = db["users"]


@user_router.post()
async def add_user(user: User):
    # Check if the user exists
    existing_user = users_collection.find_one({"name": user.name})
    if existing_user:
        raise HTTPException(
            status_code=400, detail="A user with this name already exists."
        )

    # Add user
    users_collection.insert_one(user.model_dump)

    return {"message": "User data updated successfully"}


@user_router.put("/{user_id}")
async def update_user(user_id: str, user: User):
    # Check if the user exists
    existing_user = users_collection.find_one({"_id": id})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user data
    update_data = {"$set": {"username": user.username, "password": user.password}}
    users_collection.update_one({"_id": user.id}, update_data)

    return {"message": "User data updated successfully"}
