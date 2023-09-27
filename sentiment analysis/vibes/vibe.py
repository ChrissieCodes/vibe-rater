import spacy
from spacytextblob import spacytextblob
import asent
import bleach
from cleantext import clean


nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")
nlp.add_pipe("asent_en_v1")
# TODO:sanitize python chat and make this http post
# Add polarity values to DB
# convert to channel point redemption to and Query DB


def vibe_rater(chat: str) -> dict:
    clean_text = bleach.clean(clean(chat)).replace("!", "")
    vibe = nlp(clean_text)
    polarity = vibe._.polarity
    return {
        "negative": round(polarity.negative, 3),
        "neutral": round(polarity.neutral, 3),
        "positive": round(polarity.positive, 3),
    }


def example_data(username: str, good: list, bad: list) -> dict:
    return {"username": username, "good": good, "bad": bad}


def vibe_rater_store(
    username: str, positive_score: float, negative_score: float, example_data: dict
) -> list:
    example_data["good"].append(positive_score)
    example_data["bad"].append(negative_score)
    pass
