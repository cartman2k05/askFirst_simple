from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from database import Base


class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)
    title = Column(String)

    messages = relationship(
        "Message",
        cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    thread_id = Column(
        Integer,
        ForeignKey("threads.id")
    )

    role = Column(String)
    content = Column(Text)


class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True)

    key = Column(String, unique=True)
    value = Column(Text)