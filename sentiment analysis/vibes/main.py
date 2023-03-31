from fastapi import FastAPI, Depends, HTTPException
from vibe import vibe_rater
from pydantic import BaseModel
from database import SessionLocal, engine
from schemas import Chat, Sentiment, SentimentCreate, SentimentUpdate
from sqlalchemy.orm import Session
import repository
import models
from dotenv import load_dotenv

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    # TODO: please write a unit test to decompose this issue.


@app.post("/sentiment/", response_model=Sentiment)
def new_sentiment(sentiment: SentimentCreate, db: Session = Depends(get_db)):
        return repository.create_sentiment(db=db,sentiment=sentiment)

@app.post("/sentiment/function/", response_model=Sentiment)
def new_sentiment(sentiment: SentimentCreate):
    db_sentiment = repository.create_sentiment(sentiment)
    if db_sentiment:
        raise HTTPException(status_code=400, detail="Sentiment Created")


@app.get("/sentiment/", response_model=list[Sentiment])
def read_sentiment(db: Session = Depends(get_db)):
    sentiments = repository.get_sentiment(db)
    return sentiments


@app.put("/sentiment/{username}", response_model=Sentiment)
def updated_sentiment(sentiment: SentimentUpdate, db: Session = Depends(get_db)):
    db_sentiment = repository.update_sentiment(db, sentiment=sentiment)
    print(db_sentiment)
    return db_sentiment

#this was where I left off, I was trying to aggregate the postive vibes for a user from the datatable. 
@app.get("/sentiment/{username}", response_model=Sentiment)
def read_sentiment(username: str, db: Session = Depends(get_db)):
    db_sentiment = repository.get_sentiment_by_username(db, username = Sentiment.username)
    if db_sentiment is None:
        raise HTTPException(status_code=404, detail="Sentiment Not Found")
    return db_sentiment


@app.get("/")
async def root():
    return {"message": "welcome to my chat bot"}


@app.post("/chat/")
async def add_chat(chat: Chat):
    chat_rating = vibe_rater(chat.message)
    print(chat_rating)
    return chat_rating
