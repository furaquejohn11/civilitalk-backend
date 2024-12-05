from fastapi import HTTPException, status
from sqlmodel import Session, select, or_
from schemas.inbox_schema import InboxCreate, InboxRead
from models import Inbox


class InboxRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_inbox(self, inbox_data: InboxCreate) -> Inbox:
        inbox = Inbox(
            created_by=inbox_data.created_by,
            received_by=inbox_data.received_by,
            has_chatguard=inbox_data.has_chatguard
        )

        self.session.add(inbox)
        self.session.commit()
        self.session.refresh(inbox)

        return inbox

    def get_user_inbox(self, user_id: int) -> list[Inbox]:
        inbox = self.session.exec(select(Inbox)
                                  .where(
                                    or_(
                                        Inbox.created_by == user_id,
                                        Inbox.received_by == user_id)
                                    )
                                  ).all()

        return list(inbox)
