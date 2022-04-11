from dataclasses import dataclass


@dataclass
class UserDomain:
    id: int
    username: str
    stream_token: str
    account_type: str
    getstream_id: str
