from fastapi import FastAPI
from routers import user_router, inbox_router, conversation_router
from db.db import create_db_and_tables


app = FastAPI()


# Initialize the database and tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}


app.include_router(user_router, prefix="/api/user", tags=['User'])
app.include_router(inbox_router, prefix="/api/inbox", tags=['Inbox'])
app.include_router(conversation_router, prefix="/api/conversation", tags=['Conversation'])




