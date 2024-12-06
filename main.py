from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from repositories import ConversationRepository
from routers import user_router, inbox_router, conversation_router
from db.db import create_db_and_tables, get_session
from schemas.conversation_schema import ConversationCreate
from utils.websocket_manager import ConnectionManager


app = FastAPI()


# CORS settings
origins = [
    "http://localhost",  # Allow localhost
    "http://localhost:8080",  # Allow localhost:8080
    "http://localhost:5173",  # Your frontend domain
]


# Add CORSMiddleware to allow requests from the specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use the 'origins' list defined earlier
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize the database and tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}


manager = ConnectionManager()


@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, session: Session = Depends(get_session)):
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            conversation_repository = ConversationRepository(session)

            # Save the message to the database
            conversation_data = ConversationCreate(
                inbox_id=data["inbox_id"],
                sender_id=data["sender_id"],
                text=data["text"],
                has_chatguard=data.get("has_chatguard", False)
            )
            conversation = conversation_repository.create_conversation(conversation_data)

            # Broadcast the message to all connected clients
            await manager.broadcast({
                "id": conversation.id,
                "inbox_id": conversation.inbox_id,
                "sender_id": conversation.sender_id,
                "text": conversation.text,
                "created_at": conversation.created_at.isoformat()
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)


app.include_router(user_router, prefix="/api/user", tags=['User'])
app.include_router(inbox_router, prefix="/api/inbox", tags=['Inbox'])
app.include_router(conversation_router, prefix="/api/conversation", tags=['Conversation'])




