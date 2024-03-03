import pickle
import regex as re
import warnings
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import os
import uvicorn

app = FastAPI(
    title="Multilingual Spam Detection API",
    description="This API uses a machine learning model to predict whether a given message is spam or not. The model supports various languages including Tamil, English, Malayalam, Kannada, and Telugu.",
    version="1.0",
    contact={
        "name": "Sakthi Prakash",
        "url": "https://github.com/your_username/your_repository",
        "email": "sakthiprakash403@gmail.com",
    },
    license_info={
        "name": "Your License",
        "url": "https://opensource.org/licenses/MIT",
    },
)
warnings.filterwarnings("ignore")
spam_keywords = []
greeting_words = []
with open('spam_keywords.txt', 'r', encoding='utf-8') as file:

    for line in file:
        spam_keywords.append(line.strip())
with open('greeting_words.txt', 'r', encoding='utf-8') as file:

    for line in file:
        greeting_words.append(line.strip())


def count_distinct_words(message):

    message = message.lower()
    message = ''.join(c for c in message if c.isalpha() or c.isspace())

    words = message.split()
    distinct_words = set(words)
    return len(distinct_words)


with open('model.pkl', 'rb') as file:
    clf = pickle.load(file)


def extract_features(message):

    http_pattern = re.compile(
        r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
    phone_pattern = re.compile(
        r'\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{10}')

    length = len(message)
    has_http_link = 1 if http_pattern.search(message) else 0
    has_phone_number = 1 if phone_pattern.search(message) else 0

    keywords_in_message = [
        word for word in spam_keywords if word in message.lower()]
    keywords = 1 if keywords_in_message else 0

    greeting_words_in_message = [
        word for word in greeting_words if word in message.lower()]
    has_greeting_words = 1 if greeting_words_in_message else 0

    distinct_words = count_distinct_words(message)

    return (
        has_http_link,
        has_phone_number,
        length,
        has_greeting_words,
        distinct_words,
        keywords
    )


@app.get("/")
def read_root():
    return RedirectResponse("/docs")


@app.get('/predict')
async def predict(message: str) -> dict:

    features = extract_features(message)
    prediction = clf.predict([features])
    return {"prediction": "Ham" if not prediction[0] else "Spam"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
