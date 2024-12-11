from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from repositories import ConversationRepository
from routers import user_router, inbox_router, conversation_router, chatguard_router
from db.db import create_db_and_tables, get_session
from schemas.conversation_schema import ConversationCreate
from utils.websocket_manager import ConnectionManager
from repositories import MLRepository  # Assuming you've created this import

app = FastAPI()

# CORS settings (remains the same)
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

# Add CORSMiddleware (remains the same)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

# Optional: Create a single ML repository instance at startup
ml_repository = MLRepository()


@app.websocket("/ws/chat")
async def websocket_endpoint(
        websocket: WebSocket,
        session: Session = Depends(get_session)
):
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            # Create conversation repository with pre-initialized ML repository
            conversation_repository = ConversationRepository(
                session,
                ml_repository=ml_repository
            )

            # Prepare conversation data with error handling
            try:
                conversation_data = ConversationCreate(
                    inbox_id=data["inbox_id"],
                    sender_id=data["sender_id"],
                    text=data["text"],
                    has_chatguard=data.get("has_chatguard", False)
                )
            except KeyError as e:
                # Handle missing required fields
                await websocket.send_json({
                    "error": f"Missing required field: {str(e)}"
                })
                continue
            except ValueError as e:
                # Handle validation errors
                await websocket.send_json({
                    "error": str(e)
                })
                continue

            # Create conversation with error handling
            try:
                conversation = conversation_repository.create_conversation(conversation_data)
            except Exception as e:
                # Log the error and send error response
                print(f"Conversation creation error: {e}")
                await websocket.send_json({
                    "error": "Failed to create conversation"
                })
                continue

            # Broadcast the message to all connected clients
            broadcast_data = {
                "id": conversation.id,
                "inbox_id": conversation.inbox_id,
                "sender_id": conversation.sender_id,
                "text": conversation.text,
                "created_at": conversation.created_at.isoformat()
            }

            await manager.broadcast(broadcast_data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        # Catch-all for unexpected errors
        print(f"Unexpected WebSocket error: {e}")
        await websocket.close()


# Router inclusions remain the same
app.include_router(user_router, prefix="/api/user", tags=['User'])
app.include_router(inbox_router, prefix="/api/inbox", tags=['Inbox'])
app.include_router(conversation_router, prefix="/api/conversation", tags=['Conversation'])
app.include_router(chatguard_router, prefix="/api/chatguard", tags=['Chatguard'])