# general imports
from argparse import ArgumentParser
import scipy.sparse.csr
import pandas as pd
import numpy as np
import pickle

# scikit learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.metrics import precision_score

# Text processing
from process_production_input import *

def add_features(X,emails_features):
    if not isinstance(X,pd.core.frame.DataFrame):
        if isinstance(X,scipy.sparse.csr.csr_matrix):
            X = pd.DataFrame(X.todense())
        else:
            X = pd.DataFrame(X)
    extracted_features = emails_features[0].keys()
    for extracted_feature in extracted_features:
        X[extracted_feature] = [mail[extracted_feature] for mail in emails_features]
    return X

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-f',dest='filename', help="Filename with emails json to classify")

    args = parser.parse_args()

    print "Cargando pickles..."
    vectorizer = pickle.load(open('pickle/tfidf_train.pickle','rb'))
    decomposition = pickle.load(open('pickle/pca-antes.pickle','rb'))
    classifier = pickle.load(open('pickle/RandomForest_X_pca-antes.pickle','rb'))

    "Procesando emails"
    emails_features, emails_text = features_extraction(args.filename)
    
    print "Extrayendo ngrams features..."
    X = vectorizer.transform(emails_text)

    X = add_features(X,emails_features)

    if isinstance(X,scipy.sparse.csr.csr_matrix):
        X = pd.DataFrame(X.todense())
    X = decomposition.transform(X)

    prediction = classifier.predict(X)

    print prediction

    res = pd.DataFrame(prediction)
    res.to_csv(open('resultado.csv','wb'))





