from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from argon2 import PasswordHasher
import connect

create_table = '<create_table_statement>'
sql_statements = [
    """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    salt TEXT NOT NULL,
    password TEXT NOT NULL
);"""
]

app = FastAPI()

ph = PasswordHasher()

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
async def registration(username: str = Form(...), password: str = Form(...)):
    if username in users:
        raise HTTPException(status_code=404, detail="Invalid username")
    users.append(username)
    return "Successfully registered"

