from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from argon2 import PasswordHasher
import uuid
import connect



app = FastAPI()

ph = PasswordHasher()

database = "test.db"

connect.create_db("test.db")



class user_info(BaseModel):
    username: str
    password: str


users: list[str] = []

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username not in users:
        raise HTTPException(status_code=404, detail="user is not registered")
    response_message = {"message": "the user has attempted to login", "username": username}
    return response_message

@app.post("/registration")
async def registration(
    username: str = Form(...),
    password: str = Form(...)
):
    user_id = str(uuid.uuid4())
    password_hash = ph.hash(password)

    user = (user_id, username, password_hash)


    connect.create_user(database, user)
   

    return {"message": "Successfully registered"}
