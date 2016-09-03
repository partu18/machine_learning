import string
from nltk import word_tokenize          
#from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import stopwords


###############
#   Funciones para interpretar el texto. Ejemplo:
#   txt = 'hi how are you? are you leaving now? I wanted to spend some time with you'
#	tokenize(txt) -> ['hi', u'leave', 'I', u'want', 'spend', 'time']
###############

lematizer = WordNetLemmatizer()
stop_words = stopwords.words('english')

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    tokens = [i for i in tokens if i not in string.punctuation and i not in stop_words]
    lemmas = lemmatize_tokens(pos_tag(tokens), lematizer)
    return lemmas


def lemmatize_tokens(tagged_tokens, lematizer):
    lemmatized = []
    for token_tag in tagged_tokens:
        lemmatized.append(lematizer.lemmatize(token_tag[0],penn_to_wn(token_tag[1])))
    return lemmatized


def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return wn.NOUN

def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']

def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']


def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']