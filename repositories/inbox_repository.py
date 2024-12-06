from fastapi import HTTPException, status
from sqlmodel import Session, select, or_
from schemas.inbox_schema import InboxCreate
from models import Inbox


class InboxRepository:
    def __init__(self, session: Session):
        self.session = session

    def has_existing_inbox(self, sender_id: int, receiver_id: int) -> bool:
        inbox = self.session.exec(
            select(Inbox)
            .where(
                or_(
                    (Inbox.created_by == sender_id and
                     Inbox.received_by == receiver_id),
                    (Inbox.created_by == receiver_id and
                     Inbox.received_by == sender_id)
                )
            )
        ).first()

        return True if inbox else False

    def create_inbox(self, inbox_data: InboxCreate) -> Inbox:
        # Check if there is an existing inbox between 2 users
        if self.has_existing_inbox(inbox_data.created_by,
                                   inbox_data.received_by):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inbox already exist"
            )

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
        inbox = self.session.exec(
            select(Inbox)
            .where(
                or_(
                    Inbox.created_by == user_id,
                    Inbox.received_by == user_id)
            )
            ).all()

        return list(inbox)
