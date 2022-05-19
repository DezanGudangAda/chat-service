from sqlalchemy import or_
from typing import Optional, List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from gada_chat_service.chat_service.channel.models import Channel
from gada_chat_service.core.channel.accessors.channel_accessor import IChannelAccessor
from gada_chat_service.core.channel.models import ChannelDomain
from gada_chat_service.core.channel.specs import InsertChannelSpec, CreateChannelSpec, GetChannelDbSpec


class ChannelAccessor(IChannelAccessor):
    def __init__(self):
        engine = create_engine("postgresql+psycopg2://postgres:AdminPassword123@localhost/chat")
        self._session = Session(bind=engine)
        self._query = self._session.query(Channel)

    def get_channel_by_id(self, channel_id: str) -> Optional[ChannelDomain]:
        channel = self._query.filter(Channel.id == channel_id).first()
        if channel is None:
            return None

        return channel.to_domain()

    def create_channel(self, spec: InsertChannelSpec) -> Optional[ChannelDomain]:
        new_channel = Channel()
        new_channel.id = spec.channel_id
        new_channel.channel_name = spec.channel_name
        new_channel.buyer_getstream_id = spec.buyer_getstream_id
        new_channel.seller_getstream_id = spec.seller_getstream_id

        self._session.add(new_channel)
        self._session.commit()

        return new_channel.to_domain()

    def get_channel_by_users(self, spec: GetChannelDbSpec) -> Optional[ChannelDomain]:
        chan = self._query. \
            filter(Channel.seller_getstream_id == spec.seller_getstream_id,
                   Channel.buyer_getstream_id == spec.buyer_getstream_id).first()

        if chan is None:
            return None

        return chan.to_domain()

    def get_channel_by_user(self, getstream_id: str) -> Optional[List[ChannelDomain]]:
        chan = self._query. \
            filter(or_(Channel.seller_getstream_id == getstream_id, Channel.buyer_getstream_id == getstream_id))

        if chan is None:
            return None

        res = []
        for c in chan:
            res.append(c.to_domain())

        return res
