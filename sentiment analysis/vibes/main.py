from fastapi import FastAPI, Depends, HTTPException
from vibe import vibe_rater
from pydantic import BaseModel
from database import SessionLocal, engine
from schemas import Chat, Sentiment, SentimentCreate, SentimentUpdate
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import repository
import models
from dotenv import load_dotenv
import serial


models.Base.metadata.create_all(bind=engine)
serial_conn = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPT's suggested method for lifespan is an async which yields
    inbetween setup and teardown. There is a startup and shutdown event but it's
    been deprecated :/
    """
    serial_conn = serial.Serial(
        'COM4',
        115200,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=1)
    if not serial_conn.is_open:
        serial_conn.open()
    # Ideally we would sleep for some amount of time here to give windows
    # time to flush the COM port but somehow sleep within async feels worse!
    yield
    serial_conn.close()


app = FastAPI(lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    # TODO: please write a unit test to decompose this issue.


@app.get(
    "/totals/")
def total_sentiment(db: Session = Depends(get_db)):
    return [x.to_dict() for x in repository.get_totals_by_username(db=db)]

@app.post("/sentiment/", response_model=Sentiment)
def new_sentiment(sentiment: SentimentCreate, db: Session = Depends(get_db)):
    return repository.create_sentiment(db=db, sentiment=sentiment)

@app.get("/sentiment/", response_model=list[Sentiment])
def read_sentiment(db: Session = Depends(get_db)):
    sentiments = repository.get_sentiment(db)
    return sentiments


@app.put("/sentiment/{username}", response_model=Sentiment)
def updated_sentiment(sentiment: SentimentUpdate, db: Session = Depends(get_db)):
    db_sentiment = repository.update_sentiment(db, sentiment=sentiment)
    print(db_sentiment)
    return db_sentiment


@app.get("/")
async def root():
    return {"message": "welcome to my chat bot"}


@app.post("/chat/")
async def add_chat(chat: Chat):
    chat_rating = vibe_rater(chat.message)
    print(chat_rating)
    return chat_rating


@app.get("/serial/")
def run_bubbles():
    # without a sleep, it's possible to DOS, and possibly crash the connection
    # to the serial port here. It's unlikely to cause any harm, but it may
    # require a restart of the app to recover (and perhaps the USB host).
    if not serial.is_open:
        serial_conn.open()
        # we should never need to reopen the connection here, but IFF we do
        # it will likely also require a delay before sending any data
        # time.sleep(2)

    serial_conn.write(b'q')
    serial_conn.flush()
