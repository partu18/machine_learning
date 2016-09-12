import features
import ngram_features
import mime_headers_features
import pandas as pd
import pickle
import numpy as np

from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
from helper import Helper
from inspect import getmembers, isfunction
from emailInfoExtractor import *

features_functions = [m for m in getmembers(features) if isfunction(m[1])]
ngram_features_functions = [m for m in getmembers(ngram_features) if isfunction(m[1])]
mime_headers_features_functions = [m for m in getmembers(mime_headers_features) if isfunction(m[1])]

def preprocess(raw_emails):
    return [get_email_info_structure(mail) for mail in raw_emails]

def process_email(email):
    #simple features
    final_features = {name:extractor(email) for (name,extractor) in features_functions}
    for (name, extractor) in ngram_features_functions:
        ng_features = extractor(email)
        for feature_name,value in ng_features.iteritems():
            final_features[feature_name] = value

    for (name, extractor) in mime_headers_features_functions:
        header_features = extractor(email)
        for feature_name,value in header_features.iteritems():
            final_features[feature_name] = value        

    return final_features

if __name__ == "__main__":

    helper = Helper()

    print "Leyendo jsons"
    spam_emails, ham_emails = helper.get_parsed_emails()

    print "Preprocesando spams"
    preprocessed_spams = preprocess(spam_emails)
    print "Preprocesando hams"
    preprocessed_hams = preprocess(ham_emails)


    # Extraigo atributos
    print "Extrayendo features de spam"
    processed_spams = [process_email(mail) for mail in preprocessed_spams] # Multiprocessing?
    print "Extrayendo features de ham"
    processed_hams = [process_email(mail) for mail in preprocessed_hams] # Multiprocessing?

    print "Creando dataframe.."
    df = pd.DataFrame(ham_emails+spam_emails, columns=['raw_email'])
    df['class'] = ['ham' for _ in range(len(ham_emails))]+['spam' for _ in range(len(spam_emails))]


    extracted_features = processed_hams[0].keys()
    for extracted_feature in extracted_features:  ## ESTE FOR TARDA MUCHO!!!!!
        print "Escribiendo feature " + extracted_feature
        df[extracted_feature] = [mail[extracted_feature] for mail in (processed_hams+processed_spams)]

    pickle.dump(df,open('df.pickle','w'))

    # Preparo data para clasificar
    X = df[extracted_features].values
    y = df['class']

    # Elijo mi clasificador.
    clf = DecisionTreeClassifier()

    # Ejecuto el clasificador entrenando con un esquema de cross validation
    # de 10 folds.
    res = cross_val_score(clf, X, y, cv=10)
    print np.mean(res), np.std(res)
    # salida: 0.783040309346 0.0068052434174  (o similar)


