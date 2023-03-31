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

def example_data(username: str, good : list, bad : list) -> dict:
    return {"username":username, "good":good, "bad":bad}
    

def vibe_rater_store(username: str, positive_score: float, negative_score: float, example_data : dict) -> list:
    """_retrieve the list for the username and then add the positive and negatives scores to it_ 

    Args:
        username (_type_): chatter
        positive_score (_type_): their positive score for the chat
        negative_score (_type_): their negatives score for the chat

    Returns:
        list: _description_
    """
    example_data['good'].append(positive_score)
    example_data['bad'].append(negative_score)
    pass
    

# chat_count = count(chat)
# add all polarities together and divide by chat count

# write test to check bleach clean work properly
# print(vibe_rater("!vibes exponential moving average math average test and I have a good idea what bad words to not use!"))
# print(vibe_rater("i am not the best right now"))
