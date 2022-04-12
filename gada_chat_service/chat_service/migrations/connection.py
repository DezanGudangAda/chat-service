from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def gas() -> Session:
    engine = create_engine("postgresql+psycopg2://postgres:AdminPassword123@localhost/chat")
    return engine
