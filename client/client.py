import asyncio
import websockets

async def chat_client():
    uri = "ws://localhost:8000/ws"
    
    async with websockets.connect(uri) as websocket:
        print("✅ Conectado ao servidor de chat!")


        async def receive_messages():
            while True:
                message = await websocket.recv()
                print(f"\n📩 Nova mensagem: {message}\nDigite sua mensagem: ", end="", flush=True)


        asyncio.create_task(receive_messages())

        while True:
            message = input("Digite sua mensagem ou '/play' para jogar: ")
            await websocket.send(message)

asyncio.run(chat_client())
