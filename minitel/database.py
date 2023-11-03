import logging
from sqlalchemy import create_engine, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from absl import flags


flags.DEFINE_string("db_path", "sqlite://", "Path to a database file.")


class Base(DeclarativeBase):
    pass

# 1 classified can use 3 lines of 36 chars each, i.e. 108 chars
CLASSIFIED_MAXLEN = 108
NICK_MAXLEN = 8

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
        return f"QuestEntry(id={self.id!r}, nick={self.nick!r}), quest={self.quest!r}"

    
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
