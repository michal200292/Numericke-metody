from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.probability import FreqDist
from string import punctuation
from math import sqrt
from model import ALPHABET

stop_words = set([word.lower() for word in stopwords.words('english')])
snowball_stemmer = SnowballStemmer('english')


def normalize_vector(vector):
    length = 0
    for w in vector:
        length += vector[w]**2
    length = sqrt(length)
    for w in vector:
        vector[w] /= length
    return vector


def process_text(text: str) -> dict[str, int]:
    text = "".join(list(map(lambda c: " " if c in punctuation else c, text)))
    words = [w.lower() for sentence in sent_tokenize(text) for w in word_tokenize(sentence)]
    words = filter(lambda w: w not in stop_words, words)
    words = map(snowball_stemmer.stem, words)
    words = filter(ALPHABET.__contains__, words)
    return normalize_vector(dict(FreqDist(words)))
