# -- lemmatization -- #
# !python -m spacy download de_dep_news_trf
import spacy
nlp = spacy.load('de_dep_news_trf')

def lemmatize(text):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc])

# -- stopwords -- #
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import nltk
nltk.download('stopwords')

def remove_stopwords(text):
    stop_words = set(stopwords.words('german'))
    words = word_tokenize(text)
    filtered_text = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_text)