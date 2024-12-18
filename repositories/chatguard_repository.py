from sqlmodel import Session, select, update, text
from models import Inbox, BotModel
from schemas.conversation_schema import ConversationCreate


class ChatguardRepository:

    def __init__(self, session: Session):
        self.session = session

    def enable_chatguard(self, inbox_id: int, name: str) -> ConversationCreate:
        check_chatguard = self.has_chatguard(inbox_id)
        txt: str
        if not check_chatguard:
            txt = f'Chatguard has been enabled by {name}. All profanity messages will be filtered.'
            self.chatguard_helper(inbox_id, True)
        else:
            txt = f'Chatguard is already enable. All profanity messages will be filtered.'
        prompt = ConversationCreate(
            inbox_id=inbox_id,
            sender_id=0,
            text=txt,
            has_chatguard=True,
            bot_model=self.get_chatguard_model(inbox_id)
        )
        return prompt

    def disable_chatguard(self, inbox_id: int, name: str):
        check_chatguard = self.has_chatguard(inbox_id)
        txt: str
        if check_chatguard:
            txt = f'Chatguard has been disabled by {name}. All profanity messages will not be filtered.'
            self.chatguard_helper(inbox_id, False)
        else:
            txt = f'Chatguard is already disabled. All profanity messages will not be filtered.'
        prompt = ConversationCreate(
            inbox_id=inbox_id,
            sender_id=0,
            text=txt,
            has_chatguard=True,
            bot_model=self.get_chatguard_model(inbox_id)

        )
        return prompt

    # def help_chatguard(self):

    def has_chatguard(self, inbox_id: int) -> bool:
        chatguard = self.session.exec(
            select(Inbox.has_chatguard)
            .where(Inbox.id == inbox_id)
        ).first()
        return chatguard

    def chatguard_helper(self, inbox_id: int, value: bool):
        self.session.exec(
            update(Inbox)
            .where(Inbox.id == inbox_id)
            .values(has_chatguard=value)
        )
        self.session.commit()

    def get_chatguard_model(self, inbox_id: int) -> BotModel:
        chatguard_model = self.session.exec(
            select(Inbox.bot_model)
            .where(Inbox.id == inbox_id)
        ).first()
        return chatguard_model

    def update_chatguard_model(self, inbox_id: int, value: BotModel):
        query = text("""
                UPDATE inbox
                SET bot_model = :bot_model
                WHERE id = :inbox_id
            """)
        self.session.execute(query, {"bot_model": value.value, "inbox_id": inbox_id})
        self.session.commit()

    def set_rnn_model(self, inbox_id: int, name: str) -> ConversationCreate:
        bot_model = self.get_chatguard_model(inbox_id)
        txt = str
        if bot_model != BotModel.RNN:
            self.update_chatguard_model(inbox_id, BotModel.RNN)
            txt = f'Chatguard model has been updated to RNN mode by {name}.'
        else:
            txt = "Chatguard model is already in RNN mode."

        prompt = ConversationCreate(
            inbox_id=inbox_id,
            sender_id=0,
            text=txt,
            has_chatguard=self.has_chatguard(inbox_id),
            bot_model=BotModel.RNN
        )
        return prompt

    def set_random_forest_model(self, inbox_id: int, name: str) -> ConversationCreate:
        bot_model = self.get_chatguard_model(inbox_id)
        txt = str
        if bot_model != BotModel.RANDOM_FOREST:
            self.update_chatguard_model(inbox_id, BotModel.RANDOM_FOREST)
            txt = f'Chatguard model has been updated to Random Forest mode by {name}.'
        else:
            txt = "Chatguard model is already in Random Forest mode."

        prompt = ConversationCreate(
            inbox_id=inbox_id,
            sender_id=0,
            text=txt,
            has_chatguard=self.has_chatguard(inbox_id),
            bot_model=BotModel.RANDOM_FOREST
        )
        return prompt

    def view_status(self, inbox_id: int) -> ConversationCreate:
        has_chatguard = self.has_chatguard(inbox_id)
        bot_model = self.get_chatguard_model(inbox_id)

        txt = f"Chatguard Status:\nActive: {has_chatguard}\nCurrent Model: {bot_model}"

        prompt = ConversationCreate(
            inbox_id=inbox_id,
            sender_id=0,
            text=txt,
            has_chatguard=has_chatguard,
            bot_model=bot_model
        )
        return prompt

    def view_help(self, inbox_id: int) -> ConversationCreate:
        has_chatguard = self.has_chatguard(inbox_id)
        bot_model = self.get_chatguard_model(inbox_id)

        txt = f"""Welcome to Civilitalk! I am your Chatguard bot.\n
               At your first start, chatguard is initially disabled and its default model is Random Forest\n
               Chatguard Commands:\n
               /chatguard-on     : To enable chatguard profanity filter\n
               /chatguard-off     : To disable chatguard profanity filter\n
               /chatguard-rnn    : To switch into RNN model\n
               /chatguard-rf     : To switch into Random Forest model\n
               /chatguard-status : To view status of activation and model\n
               /chatguard-help   : To view this page\n
           """

        prompt = ConversationCreate(
            inbox_id=inbox_id,
            sender_id=0,
            text=txt,
            has_chatguard=has_chatguard,
            bot_model=bot_model
        )
        return prompt
