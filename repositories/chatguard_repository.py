from sqlmodel import Session, select
from models import Inbox
from schemas.conversation_schema import ConversationCreate


class ChatguardRepository:

    def __init__(self, session: Session):
        self.session = session

    def enable_chatguard(self, inbox_id: int, name: str) -> ConversationCreate:
        check_chatguard = self.has_chatguard(inbox_id)
        txt: str
        if check_chatguard:
            txt = f'Chatguard has been enabled by {name}. All profanity messages will be filtered.'
        else:
            txt = f'Chatguard is already enable. All profanity messages will be filtered.'
        prompt = ConversationCreate(
            inbox_id=inbox_id,
            sender_id=0,
            text=txt,
            has_chatguard=True
        )
        return prompt

    def disable_chatguard(self, inbox_id: int, name: str):
        check_chatguard = self.has_chatguard(inbox_id)
        txt: str
        if not check_chatguard:
            txt = f'Chatguard has been disabled by {name}. All profanity messages will not be filtered.'
        else:
            txt = f'Chatguard is already disabled. All profanity messages will not be filtered.'
        prompt = ConversationCreate(
            inbox_id=inbox_id,
            sender_id=0,
            text=txt,
            has_chatguard=True
        )
        return prompt

    # def help_chatguard(self):

    def has_chatguard(self, inbox_id: int) -> bool:
        chatguard = self.session.exec(
            select(Inbox.has_chatguard)
            .where(Inbox.id == inbox_id)
        )
        return bool(chatguard)

    # def send_prompt(self, prompt_data: ConversationCreate):
