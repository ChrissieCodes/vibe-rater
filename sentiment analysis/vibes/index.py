import spacy
from spacytextblob import spacytextblob
import pandas


nlp = spacy.load("en_core_web_md")
# df = pandas.read_table("./sentiment-analysis-on-movie-reviews/train.tsv.zip")
nlp.add_pipe("spacytextblob")

text = "you are awesome. i'm loving this stinky chat you all rock this is awesome we can hang out together all day i do not want to leave"
text2 = "you are not bad I want you to go away"
doc = nlp(text)
doc2 = nlp(text2)
polarity = doc._.blob.polarity
print(f"polarity = {polarity}")
polarity = doc2._.blob.polarity
print(f"polarity2 = {polarity}")
subjectivity = doc._.blob.subjectivity
print(f"subjectivity = {subjectivity}")
subjectivity = doc2._.blob.subjectivity
print(f"subjectivity2 = {subjectivity}")

# chat_count = count(chat)
# add all polarities together and divide by chat count