# user_routes.py

from eyes_to_read_be.common.config import MONGO_URI
from eyes_to_read_be.common.hash import Hash
from fastapi import APIRouter, FastAPI, HTTPException, Depends, Request, status
from eyes_to_read_be.common.oauth import get_current_user
from eyes_to_read_be.common.jwttoken import create_access_token
from eyes_to_read_be.common.models import User, Login, Token, TokenData
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

user_router = APIRouter(prefix="/users")

client = MongoClient(MONGO_URI)
db = client["eyes_to_see_db"]
users_collection = db["users"]


@user_router.post("/register")
def create_user(request: User):
    hashed_pass = Hash.bcrypt(request.password)
    user_object = dict(request)
    user_object["password"] = hashed_pass
    users_collection.insert_one(user_object)
    return {"result": "created"}


@user_router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"username": request.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
