import json
from pathlib import Path

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

GREETINGS = {"hi", "hello", "hey", "hola", "greetings"}
FAREWELLS = {"bye", "goodbye", "thanks", "thank", "thankyou"}
FALLBACK = "Sorry, I could not find an answer to that. Please try rephrasing your question or contact support@shopease.com."


def download_resources():
    for package, path in [("stopwords", "corpora/stopwords"), ("wordnet", "corpora/wordnet")]:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(package, quiet=True)


class FAQChatbot:
    def __init__(self, faq_file="faqs.json", threshold=0.2):
        download_resources()
        self.threshold = threshold
        self.tokenizer = RegexpTokenizer(r"[a-z0-9]+")
        self.stop_words = set(stopwords.words("english")) - {"not", "no"}
        self.lemmatizer = WordNetLemmatizer()

        path = Path(__file__).parent / faq_file
        with open(path, encoding="utf-8") as file:
            self.faqs = json.load(file)

        self.questions = [item["question"] for item in self.faqs]
        self.answers = [item["answer"] for item in self.faqs]
        self.keywords = [item.get("keywords", "") for item in self.faqs]

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([self.preprocess(q + " " + k) for q, k in zip(self.questions, self.keywords)])

    def preprocess(self, text):
        tokens = self.tokenizer.tokenize(text.lower())
        tokens = [t for t in tokens if t not in self.stop_words]
        return " ".join(self.lemmatizer.lemmatize(t) for t in tokens)

    def reply(self, message):
        words = set(self.tokenizer.tokenize(message.lower()))
        if words and len(words) <= 3 and words & GREETINGS:
            return "Hello! I am the ShopEase assistant. Ask me anything about orders, shipping, returns or payments.", 1.0
        if words and len(words) <= 5 and words & FAREWELLS:
            return "You are welcome! Have a great day.", 1.0

        cleaned = self.preprocess(message)
        if not cleaned:
            return FALLBACK, 0.0

        vector = self.vectorizer.transform([cleaned])
        scores = cosine_similarity(vector, self.matrix)[0]
        best = int(scores.argmax())

        if scores[best] < self.threshold:
            return FALLBACK, float(scores[best])
        return self.answers[best], float(scores[best])
