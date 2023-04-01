from sqlalchemy.orm import Session
from sqlalchemy import func

from models import Sentiment
import schemas


def get_sentiment(db: Session):
    return db.query(Sentiment).all()


def get_sentiment_by_username(db: Session, username: str):
    return db.query(Sentiment).filter(Sentiment.username == username).first()


def create_sentiment(db: Session, sentiment: schemas.SentimentCreate):
    db_sentiment = Sentiment(**sentiment.dict())
    print(db_sentiment.__dict__)
    db.add(db_sentiment)
    db.commit()
    db.refresh(db_sentiment)
    return db_sentiment


def update_sentiment(db: Session, sentiment: schemas.SentimentCreate):
    db_sentiment = (
        Sentiment.query
            .filter(Sentiment.username==sentiment.username)
            .update(username=sentiment.username,
                    positive=sentiment.positive,
                    neutral=sentiment.neutral,
                    negative=sentiment.negative,
                    number_of_chats=sentiment.number_of_chats,
                    syncronize_session='fetch')
    )
    db.commit()
    db.refresh(db_sentiment)
    return db_sentiment


def get_totals_by_username(db: Session):
    return (Sentiment.query(func.sum(Sentiment.vibe_sum))
            .group_by(Sentiment.username))

