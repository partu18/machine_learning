# general imports
from argparse import ArgumentParser
import pandas as pd
import numpy as np
import pickle

# scikit learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score

# Text processing
from process_input import *

def add_features(X,ham_features,spam_features):
    X = pd.DataFrame(X.todense())
    extracted_features = ham_features[0].keys()
    for extracted_feature in extracted_features:
        X[extracted_feature] = [mail[extracted_feature] for mail in (ham_features+spam_features)]
    return X

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-v',dest='vectorizer', default='vectorizer', help="Name of the tf-idf vectorizer pickle file.")
    parser.add_argument('-d',dest='decomposition', choices=['pca-antes','pca-despues','pca-despues','svd-antes','svd-despues'], help="Name of the nklearn decomposition reductor pickle file.")
    parser.add_argument('-c',dest='classifier', choices=['RandomForest','KNN','Tree','NB','SVM','MNB'], help="Name of the classifier to use.")

    args = parser.parse_args()

    if not args.classifier or not args.decomposition:
        parser.error("Missing parameters")

    print "Cargando pickles..."
    vectorizer = pickle.load(open('pickle/{}.pickle'.format(args.vectorizer),'rb'))
    decomposition = pickle.load(open('pickle/{}.pickle'.format(args.decomposition),'rb'))
    classifier = pickle.load(open('pickle/{}.pickle'.format(args.classifier+'_X_'+args.decomposition),'rb'))

    "Procesando emails"
    ham_features, spam_features, hams_text, spams_text = features_extraction()
    
    print "Extrayendo ngrams features..."
    X = vectorizer.transform(hams_text+spams_text)

    if 'antes' in args.decomposition:
        print "Agregando otras features extraidas..."
        X = add_features(X,ham_features,spam_features)

    print "reduciendo dimensionalidad..."
    X = decomposition.transform(X)

    if 'despues' in args.decomposition:
        print "Agregando otras features extraidas..."
        X = add_features(X,ham_features,spam_features)
    
    print "Extrayendo las clases..."
    y = ['ham' for _ in range(len(hams_text))]+['spam' for _ in range(len(spams_text))]

    prediction = classifier.predict(X)
    print "accuracy: ", accuracy_score(y, prediction)