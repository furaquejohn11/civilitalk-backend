from typing import List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection and add it to the active connections."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection from the active connections."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"Disconnected: {websocket.client}")

    async def broadcast(self, message: dict):
        """Send a message to all active WebSocket connections."""
        disconnected_clients = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to {connection.client}: {e}")
                disconnected_clients.append(connection)

        # Clean up disconnected clients
        for connection in disconnected_clients:
            self.disconnect(connection)
