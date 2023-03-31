from sqlalchemy import Column, Float, Integer, String

from database import Base


class Sentiment(Base):
    __tablename__ = "sentiment"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True)
    positive = Column(Float)
    neutral = Column(Float)
    negative = Column(Float)
    number_of_chats = Column(Integer)
    vibe_sum = Column(Integer, positive - negative)
