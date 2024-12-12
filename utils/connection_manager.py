from typing import List, Dict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, inbox_id: int):
        """Accept a new WebSocket connection and associate it with an inbox_id."""
        await websocket.accept()
        if inbox_id not in self.connections:
            self.connections[inbox_id] = []
        self.connections[inbox_id].append(websocket)
        print(f"Connected to inbox {inbox_id}: {websocket.client}")

    def disconnect(self, websocket: WebSocket, inbox_id: int):
        """Remove a WebSocket connection from the specific inbox."""
        if inbox_id in self.connections and websocket in self.connections[inbox_id]:
            self.connections[inbox_id].remove(websocket)
            if not self.connections[inbox_id]:  # Remove the key if no connections left
                del self.connections[inbox_id]
            print(f"Disconnected from inbox {inbox_id}: {websocket.client}")

    async def broadcast(self, inbox_id: int, message: dict):
        """Send a message to all WebSocket connections associated with the inbox_id."""
        if inbox_id not in self.connections:
            print(f"No clients to broadcast to for inbox {inbox_id}")
            return

        disconnected_clients = []
        for connection in self.connections[inbox_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to {connection.client}: {e}")
                disconnected_clients.append(connection)

        # Clean up disconnected clients
        for connection in disconnected_clients:
            self.disconnect(connection, inbox_id)
