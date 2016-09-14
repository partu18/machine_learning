from constants import EMAIL_TEXT
import ngrams as ng
import json

def get_1grams_features(email_structure, separator='partugabylao'):
    features_count = dict()
    email_ngrams = ng.find_ngrams(email_structure[EMAIL_TEXT], n=1, separator=separator)
    features = json.load(open('ngram_features/1grams.json'))
    for ft in features:
       features_count[ft] = email_ngrams.count(ft)
    return features_count

# def get_2grams_features(email_structure, separator='partugabylao'):
#     features_count = dict()
#     email_ngrams = ng.find_ngrams(email_structure[EMAIL_TEXT], n=2, separator=separator)
#     features = json.load(open('ngram_features/2grams.json'))
#     for ft in features:
#         features_count[ft] = email_ngrams.count(ft)
#     return features_count

# def get_3grams_features(email_structure, separator='partugabylao'):
#     features_count = dict()
#     email_ngrams = ng.find_ngrams(email_structure[EMAIL_TEXT], n=3, separator=separator)
#     features = json.load(open('ngram_features/3grams.json'))
#     for ft in features:
#         features_count[ft] = email_ngrams.count(ft)
#     return features_count

# def get_4grams_features(email_structure, separator='partugabylao'):
#     features_count = dict()
#     email_ngrams = ng.find_ngrams(email_structure[EMAIL_TEXT], n=4, separator=separator)
#     features = json.load(open('ngram_features/4grams.json'))
#     for ft in features:
#         features_count[ft] = email_ngrams.count(ft)
#     return features_count

# def get_5grams_features(email_structure, separator='partugabylao'):
#     features_count = dict()
#     email_ngrams = ng.find_ngrams(email_structure[EMAIL_TEXT], n=5, separator=separator)
#     features = json.load(open('ngram_features/5grams.json'))
#     for ft in features:
#         features_count[ft] = email_ngrams.count(ft)
#     return features_count

# def get_7grams_features(email_structure, separator='partugabylao'):
#     features_count = dict()
#     email_ngrams = ng.find_ngrams(email_structure[EMAIL_TEXT], n=7, separator=separator)
#     features = json.load(open('ngram_features/7grams.json'))
#     for ft in features:
#         features_count[ft] = email_ngrams.count(ft)
#     return features_count

# def get_10grams_features(email_structure, separator='partugabylao'):
#     features_count = dict()
#     email_ngrams = ng.find_ngrams(email_structure[EMAIL_TEXT], n=10, separator=separator)
#     features = json.load(open('ngram_features/10grams.json'))
#     for ft in features:
#         features_count[ft] = email_ngrams.count(ft)
#     return features_count