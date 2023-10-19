import logging
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

# 1 classified can use 3 lines of 36 chars each, i.e. 108 chars
CLASSIFIED_MAXLEN = 108

class Classified(Base):
    __tablename__ = "classifieds"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    contents: Mapped[str] = mapped_column(String(CLASSIFIED_MAXLEN))

    def __repr__(self) -> str:
        return f"Classified(id={self.id!r}, contents={self.contents!r})"


engine = None
    
def GetEngine():
    global engine
    # TODO get the DB path from env?
    if engine is None:
        engine = create_engine("sqlite:///test.db")
    return engine


def Migrate():
    engine = GetEngine()
    Base.metadata.create_all(engine)
