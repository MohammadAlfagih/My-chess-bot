from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import asyncio

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []


    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

maneger = ConnectionManager()

@app.websocket("/ws/play")
async def websocket_endpoint(websocket: WebSocket):
    await maneger.connect(websocket)
    print("New connction")
    
    try: 
        while True:
            data = await websocket.receive_text()
            print(f"player move {data}")

            await maneger.send_personal_message(json.dumps({"status":"thinking"}),websocket)
            await asyncio.sleep(2)

            bot_move ='e7e5'
            print(f"bot move {bot_move}")

            response = {
                "status": "success",
                "bot_move": bot_move
            }
            await maneger.send_personal_message(json.dumps(response), websocket)
    except WebSocketDisconnect:
        maneger.disconnect(websocket)
        print("🔴 العميل قطع الاتصال.")       