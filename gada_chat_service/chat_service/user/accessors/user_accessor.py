from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from gada_chat_service.chat_service.user.models import User
from gada_chat_service.core.user.accessor.user_accessor import IUserAccessor
from gada_chat_service.core.user.models import UserDomain
from gada_chat_service.core.user.specs import InsertUserTokenSpec, GetUserTokenSpec


class UserAccessor(IUserAccessor):
    def __init__(self):
        engine = create_engine("postgresql+psycopg2://postgres:AdminPassword123@localhost/chat")
        self._session = Session(bind=engine)
        self._query = self._session.query(User)

    def get_user_by_username_and_type(self, spec: GetUserTokenSpec) -> Optional[UserDomain]:
        user = self._query.\
            filter(User.username == spec.username, User.account_type == spec.type.value).first()

        if user is None:
            return None

        return user.to_domain()

    def create_user_and_token(self, spec: InsertUserTokenSpec) -> Optional[UserDomain]:
        new_user = User()
        new_user.username = spec.username
        new_user.account_type = spec.type.value
        new_user.stream_token = spec.token
        new_user.getstream_id = spec.getstream_id

        self._session.add(new_user)
        self._session.commit()

        return new_user.to_domain()

    def get_user_by_getstream_id(self, getstream_id: str) -> Optional[UserDomain]:
        user = self._query. \
            filter(User.getstream_id == getstream_id).first()

        if user is None:
            return None

        return user.to_domain()
