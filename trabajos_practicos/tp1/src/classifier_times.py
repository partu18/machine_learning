# general imports
from argparse import ArgumentParser
import scipy.sparse.csr
import pandas as pd
import numpy as np
import pickle
import time

# scikit learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score

# Text processing
from process_input import *

def add_features(X,ham_features,spam_features):
    if not isinstance(X,pd.core.frame.DataFrame):
        if isinstance(X,scipy.sparse.csr.csr_matrix):
            X = pd.DataFrame(X.todense())
        else:
            X = pd.DataFrame(X)
    extracted_features = ham_features[0].keys()
    for extracted_feature in extracted_features:
        X[extracted_feature] = [mail[extracted_feature] for mail in (ham_features+spam_features)]
    return X

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-v',dest='vectorizer', default='vectorizer', help="Name of the tf-idf vectorizer pickle file.")
    args = parser.parse_args()    

    print "Cargando vectorizer pickle..."
    vectorizer = pickle.load(open('pickle/{}.pickle'.format(args.vectorizer),'rb'))

    "Procesando emails"
    ham_features, spam_features, hams_text, spams_text = features_extraction()
    
    print "Extrayendo ngrams features..."
    X = vectorizer.transform(hams_text+spams_text)
    
    
    print "Corriendo clasificadores y tomando tiempos"
    classifiers = ["KNN","NB","RandomForest","Tree","SVM"]
    decompositions = ["pca-antes","pca-despues","svd-antes","svd-despues"]

    print "Classifier,decomposition,dataset_size,feature_amounts,prediction_time"
    for d in decompositions:
        decomposition = pickle.load(open('pickle/{}.pickle'.format(d),'rb'))
        if 'antes' in d:
            X_antes = add_features(X,ham_features,spam_features)
            X_antes = decomposition.transform(X_antes)
            X_antes = pd.DataFrame(X_antes)
        else:
            X_despues = decomposition.transform(X.todense())
            X_despues = add_features(X_despues,ham_features,spam_features)
        for c in classifiers:
            classifier = pickle.load(open('pickle/{}.pickle'.format(c+'_X_'+d),'rb'))
            X_to_use = X_antes if 'antes' in d else X_despues
            start_time = time.clock()
            prediction = classifier.predict(X_to_use)
            print c,d,X_to_use.shape[0],X_to_use.shape[1],time.clock()-start_time