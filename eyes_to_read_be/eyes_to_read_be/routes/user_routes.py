# user_routes.py

import bcrypt
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pymongo import MongoClient
from eyes_to_read_be.common.config import MONGO_URI
from eyes_to_read_be.common.models import User, UserInDB, Token, TokenData
from eyes_to_read_be.common.auth import *
from bson import ObjectId  # Required to work with MongoDB ObjectId
import jwt
from datetime import datetime, timedelta

user_router = APIRouter(prefix="/users")

client = MongoClient(MONGO_URI)
db = client["eyes_to_see_db"]
users_collection = db["users"]


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        token_data = TokenData(username=username)
    except jwt.JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )

    user = users_collection.find_one({"username": token_data.username})
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )

    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@user_router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"username": form_data.username})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not bcrypt.verify(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/me", response_model=User)
async def get_my_user(user: UserInDB = Depends(get_current_user)):
    return user


@user_router.get("/all")
async def get_users(limit: int = 10, skip: int = 0):
    users_data = users_collection.find().limit(limit).skip(skip)
    return [
        User(user_data["username"], user_data["password_hash"])
        for user_data in users_data
        if "username" and "password_hash" in user_data.keys()
    ]


@user_router.get("/{user_id}", response_model=User)
async def get_user(user_id: ObjectId):
    user = users_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(404, "User not found")

    return User(**user)


@user_router.post("", response_model=UserInDB)
async def create_user(user: User):
    existing = users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username taken")
    user.password_hash = bcrypt.hash(user.password)
    new_user = users_collection.insert_one(user.dict())
    return new_user


@user_router.put("/{user_id}")
async def update_user(user_id: ObjectId, user: User):
    # Check if the user exists
    existing_user = users_collection.find_one({"_id": user_id})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    updates = user.modeldump(exclude_unset=True)
    updated_user = existing_user.find_one_and_update(
        {"_id": id}, {"$set": updates}, return_document=True
    )
    if not updated_user:
        raise HTTPException(404)
    return updated_user


@user_router.delete("/{user_id}")
async def delete_user(user_id: str):
    # Check if the user exists
    existing_user = users_collection.find_one({"_id": user_id})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete user
    users_collection.delete_one({"_id": user_id})

    return {"message": "User deleted successfully"}
