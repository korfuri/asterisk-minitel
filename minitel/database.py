import datetime
import logging
from sqlalchemy import create_engine, String, DateTime, UniqueConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from absl import flags


flags.DEFINE_string("db_path", "sqlite://", "Path to a database file.")


class Base(DeclarativeBase):
    pass

# 1 classified can use 3 lines of 36 chars each, i.e. 108 chars
CLASSIFIED_MAXLEN = 108
NICK_MAXLEN = 8
CHATMSG_MAXLEN = 30

class Classified(Base):
    __tablename__ = "classifieds"

    id: Mapped[int] = mapped_column(primary_key=True)
    contents: Mapped[str] = mapped_column(String(CLASSIFIED_MAXLEN))

    def __repr__(self) -> str:
        return f"Classified(id={self.id!r}, contents={self.contents!r})"


class QuestEntry(Base):
    __tablename__ = "quest_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    nick: Mapped[str] = mapped_column(String(NICK_MAXLEN))
    quest: Mapped[str] = mapped_column(String)
    __table_args__ = (
        UniqueConstraint("nick", "quest"),
    )

    def __repr__(self) -> str:
        return f"QuestEntry(id={self.id!r}, nick={self.nick!r}, quest={self.quest!r})"


class QuestOwnership(Base):
    __tablename__ = "quest_ownerships"

    quest: Mapped[str] = mapped_column(String, primary_key=True)
    nick: Mapped[str] = mapped_column(String(NICK_MAXLEN))

    def __repr__(self) -> str:
        return f"QuestOwnership(quest={self.quest!r}, nick={self.nick!r})"


class ChatMessage(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    nick: Mapped[str] = mapped_column(String(NICK_MAXLEN))
    channel: Mapped[str] = mapped_column(String)
    message: Mapped[str] = mapped_column(String(CHATMSG_MAXLEN))

    def __repr__(self) -> str:
        return f"ChatMessage(id={self.id!r}, created_at={self.created_at!r}, nick={self.nick!r}), channel={self.channel!r}, message={self.message!r}"


class WantedPosting(Base):
    __tablename__ = "wanted_notices"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String(19))
    statut: Mapped[str] = mapped_column(String(19))
    contact: Mapped[str] = mapped_column(String(19))
    instructions: Mapped[str] = mapped_column(String(19*4))

class WikiArticle(Base):
    __tablename__ = "wiki_articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)  # TODO maxlength
    contents: Mapped[str] = mapped_column(String)
    is_quest: Mapped[bool] = mapped_column(Boolean)

    __table_args__ = (
        UniqueConstraint("title"),
    )


engine = None

def GetEngine(db_path=None):
    global engine
    if engine is None:
        if db_path is None:
            db_path = flags.FLAGS.db_path
        engine = create_engine(db_path)
    return engine


def Migrate():
    engine = GetEngine()
    Base.metadata.create_all(engine)
