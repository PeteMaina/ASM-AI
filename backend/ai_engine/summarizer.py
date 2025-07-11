# backend/ai_engine/summarizer.py

#pip install python-docx docx2txt PyPDF2


import re
import heapq
import nltk

nltk.download("punkt")
nltk.download("stopwords")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def summarize(text, num_sentences=5):
    text = re.sub(r'\s+', ' ', text)

    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text.lower())

    freq = {}
    for word in words:
        if word not in stop_words and word.isalnum():
            freq[word] = freq.get(word, 0) + 1

    sentences = sent_tokenize(text)
    scores = {}

    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in freq:
                scores[sent] = scores.get(sent, 0) + freq[word]

    summary = heapq.nlargest(num_sentences, scores, key=scores.get)
    return " ".join(summary)
