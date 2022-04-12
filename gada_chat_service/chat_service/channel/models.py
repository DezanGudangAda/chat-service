from sqlalchemy import Column, String, Integer

from gada_chat_service.chat_service.base.models import Base
from gada_chat_service.core.channel.models import ChannelDomain
from gada_chat_service.core.commons.utils import ObjectMapperUtil


class Channel(Base):
    __tablename__ = "channel"
    id = Column(String, primary_key=True, index=True)

    buyer_getstream_id = Column(String)
    seller_getstream_id = Column(String)
    channel_name = Column(String, index=True)

    def to_domain(self) -> ChannelDomain:
        domain = ObjectMapperUtil.map(self, ChannelDomain)
        return domain
