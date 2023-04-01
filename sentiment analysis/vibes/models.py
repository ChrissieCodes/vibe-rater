from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property

from database import Base


class Sentiment(Base):
    __tablename__ = "sentiment"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True)
    positive = Column(Float)
    neutral = Column(Float)
    negative = Column(Float)
    number_of_chats = Column(Integer)

    def __init__(self, positive, negative):
        self.positive = positive
        self.negative = negative

    @hybrid_property
    def vibe_sum(self):
        return self.positive - self.negative

