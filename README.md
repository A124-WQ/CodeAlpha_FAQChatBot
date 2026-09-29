# CodeAlpha FAQ Chatbot

A chatbot that answers customer FAQs for an online store using NLP.

## How It Works
1. FAQs are stored in `faqs.json` (questions and answers).
2. Text is preprocessed with NLTK: lowercasing, tokenizing, stop word removal and lemmatization.
3. Questions are converted to TF-IDF vectors.
4. The user's message is compared with every FAQ using cosine similarity.
5. The best matching answer is shown in a chat interface. If the match is too weak, a fallback message is shown.

## Tech Stack
Python, NLTK, scikit-learn, Streamlit

## How to Run
```
pip install -r requirements.txt
streamlit run app.py
```

## Customize
Replace the entries in `faqs.json` with FAQs for any product or topic.

## Internship
Built as part of the CodeAlpha Artificial Intelligence Internship (Task 2).
