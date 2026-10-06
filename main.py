from fastapi import FastAPI, Form, HTTPException
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import sqlite3




app = FastAPI()
ph = PasswordHasher()

database = "test.db"

try:
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
        )
        """
        )
        conn.commit()
except sqlite3.OperationalError as e:
    print(e)

@app.post("/registration")
async def registration(
    username: str = Form(...),
    password: str = Form(...)
):
    try:
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            hashed = ph.hash(password)
            cursor.execute(''' INSERT INTO users(username, password_hash) VALUES(?, ?) ''',
                           (username, hashed))

    except sqlite3.IntegrityError:
        raise HTTPException(status_code=404, detail="Username is already taken")
    

@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...)
):
    
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,))

        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="User not found")
    try:
        stored_hash = row[0]
        ph.verify(stored_hash, password)
        return {"message": "Login successful"}
    except VerifyMismatchError:
        raise HTTPException(status_code=404, detail="Incorrect password")