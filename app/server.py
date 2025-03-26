from fastapi import FastAPI, websockets, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
from models import User

app = FastAPI()
client = []

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: websockets.WebSocket, username: str, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    client.append({"username": username, "ws": websocket})

    while True:
        data = await websocket.receive_text()
        if data.startswith("/play"):
            await start_game(username, websocket, db)
        else: 
            for client in client:
                await client["ws"].send(f"{username}: {data}")
            