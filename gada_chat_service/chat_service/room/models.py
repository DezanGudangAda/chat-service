from sqlalchemy import Column, String, Integer

from gada_chat_service.chat_service.base.models import Base


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, autoincrement=True)

    buyer_id = Column(String)
    seller_id = Column(String)
    channel_name = Column(String)
