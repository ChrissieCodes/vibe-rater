from flask import Flask, request
from vibe import vibe_rater
from database import SessionLocal, engine
import repository
import models
import serial
import serial.tools.list_ports
import time

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)


db = SessionLocal()


@app.route("/totals/", methods=["GET"])
def total_sentiment():
    return [x.to_dict() for x in repository.get_totals_by_username(db=db)]


@app.route("/sentiment/", methods=["POST"])
def new_sentiment():
    return repository.create_sentiment(db=db, sentiment=request.json).to_dict()


@app.route("/sentiment/", methods=["GET"])
def read_sentiment():
    return [sentiment.to_dict() for sentiment in repository.get_sentiment(db)]


@app.route("/sentiment/", methods=["POST"])
def updated_sentiment():
    db_sentiment = repository.update_sentiment(db, sentiment=request.json)
    return db_sentiment


@app.route("/", methods=["GET"])
def root():
    return {"message": "welcome to my vibe rater"}


@app.route("/chat/", methods=["POST"])
def add_chat():
    print(request.json["message"])
    chat_rating = vibe_rater(request.json["message"])
    return chat_rating


@app.route("/serial/", methods=["GET"])
def run_bubbles():
    with serial.Serial(
        "COM4", 115200, bytesize=8, parity="N", stopbits=1, timeout=1
    ) as ser:
        time.sleep(4)
        ser.write(b"q")
        ser.flush()


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
    
