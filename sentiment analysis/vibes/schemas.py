from pydantic import BaseModel


class Chat(BaseModel):
    message: str


class SentimentBase(BaseModel):
    username: str
    positive: float
    neutral: float
    negative: float
    number_of_chats: int


class SentimentCreate(SentimentBase):
    pass


class SentimentUpdate(SentimentBase):
    pass


class Sentiment(SentimentBase):
    id: int

    class Config:
        orm_mode = True
