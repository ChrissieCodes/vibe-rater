from sqlalchemy import Column, Float, Integer, String, DateTime, Boolean, func, select
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from datetime import datetime
from sqlalchemy.orm import column_property

from database import Base


class Sentiment(Base):
    __tablename__ = "sentiment"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True)
    positive = Column(Float)
    neutral = Column(Float)
    negative = Column(Float)
    number_of_chats = Column(Integer)
    vibe_sum = column_property(positive - negative)

    @hybrid_property
    def vibe_total(self):
        return sum(vibe for vibe in "Sentiment")

    @vibe_total.expression
    def vibe_total(cls):
        return select(func.sum("Sentiment".vibe_sum))

    @hybrid_method
    def to_dict(self):
        return {"username": self.username, "vibe_total": self.vibe_sum}

class Session(Base):
    __tablename__ = "session"
    
    id= Column(Integer, primary_key=True, index=True, autoincrement=True)
    start = Column(DateTime, default = datetime.datetime.now(datetime.timezone.utc))
    end = Column(DateTime)
    status = Column(Boolean)
    
    

    