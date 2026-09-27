from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    response_message = {"message": "the user has attempted to login", "username": username}
    return response_message



