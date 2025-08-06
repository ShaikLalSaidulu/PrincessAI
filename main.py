import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from search_engine import search_query
from utils import format_results

app = FastAPI()

# Store all connected WebSocket clients
connected_clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = id(websocket)
    connected_clients.add(websocket)
    print(f"✅ Client connected: {client_id} | Total: {len(connected_clients)}")

    try:
        while True:
            # Receive voice command from client
            data = await websocket.receive_text()
            print(f"🎤 Received command: {data}")

            # Perform search (limit results to 5)
            results = search_query(data, max_results=5)

            # Format results for frontend
            formatted = format_results(results)

            # Send results to the same client
            await websocket.send_text(json.dumps(formatted, ensure_ascii=False))

    except WebSocketDisconnect:
        print(f"❌ Client disconnected: {client_id}")
        connected_clients.remove(websocket)

    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        if websocket in connected_clients:
            connected_clients.remove(websocket)