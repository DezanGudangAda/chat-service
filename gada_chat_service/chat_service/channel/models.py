from sqlalchemy import Column, String, Integer

from gada_chat_service.chat_service.base.models import Base


class Channel(Base):
    __tablename__ = "channel"
    id = Column(String, primary_key=True, index=True)

    buyer_id = Column(String)
    seller_id = Column(String)
    channel_name = Column(String, index=True)
