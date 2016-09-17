#import ngram_features
import mime_headers_features
from random import randint
import pandas as pd
import numpy as np
import pickle

# sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import PCA
from sklearn.grid_search import GridSearchCV

# Text processing
from inspect import getmembers, isfunction
from emailInfoExtractor import *
from helper import Helper
import features


features_functions = [m for m in getmembers(features) if isfunction(m[1])]
#ngram_features_functions = [m for m in getmembers(ngram_features) if isfunction(m[1])]
mime_headers_features_functions = [m for m in getmembers(mime_headers_features) if isfunction(m[1])]

def local_grid_search(X,y,curr_depth,curr_features,feature_amount,neighbor_depth=1):
    local_params = dict()
    local_params['splitter'] = ['best','random']
    local_params['max_features'] = range(max(curr_features-neighbor_depth,1),min(curr_features+neighbor_depth+1,feature_amount))
    local_params['max_depth'] = range(max(curr_depth-neighbor_depth,1),curr_depth+neighbor_depth+1)
    return grid.fit(X,y)


def grid_search(X,y,clasificators,params_grids):
    
    for clf in clasificators:
        grid = GridSearchCV(clf, local_params, cv=10)
    grid = local_grid_search(X,y,curr_depth,curr_features,feature_amount)
    print grid.best_score_, last_score
    print grid.best_params_

    ## start local search
    while grid.best_score_ > last_score:
        last_score = grid.best_score_
        grid = local_grid_search(X,y,grid.best_params_['max_depth'],grid.best_params_['max_features'],feature_amount)
        print grid.best_score_, last_score
        print grid.best_params_

    return grid

def preprocess(raw_emails):
    return [get_email_info_structure(mail) for mail in raw_emails]

def process_email(email):
    #simple features
    final_features = {name:extractor(email) for (name,extractor) in features_functions}
    #for (name, extractor) in ngram_features_functions:
    #    ng_features = extractor(email)
    #    for feature_name,value in ng_features.iteritems():
    #        final_features[feature_name] = value

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

    print "Contruyendo el vector con las clases"
    y = ['ham' for _ in range(len(ham_emails))]+['spam' for _ in range(len(spam_emails))]

    print "Creando dataframe.."
    vectorizer = TfidfVectorizer(ngram_range=(1,3),stop_words='english',max_features=5000)
    email_texts = [email[EMAIL_TEXT] for email in preprocessed_hams+preprocessed_spams]
    X_train = vectorizer.fit_transform(email_texts)

    ## SVD
    svd = TruncatedSVD(n_components=100, random_state=42)
    X_svd_transformed = svd.fit_transform(X_train)
    X_svd = pd.DataFrame(X_svd_transformed)

    ## PCA
    pca = PCA(n_components=100, whiten=True)
    X_pca_transformed = pca.fit_transform(X_train.todense())
    X_pca = pd.DataFrame(X_pca_transformed)

    extracted_features = processed_hams[0].keys()
    for extracted_feature in extracted_features: 
        print "Escribiendo feature " + extracted_feature
        X_svd[extracted_feature] = [mail[extracted_feature] for mail in (processed_hams+processed_spams)]
        X_pca[extracted_feature] = [mail[extracted_feature] for mail in (processed_hams+processed_spams)]


    #print haciendo pickle del svd y del dataframe
    pickle.dump(y,open('y.pickle','w'))
    pickle.dump(X_svd,open('X_svd-despues.pickle','w'))
    pickle.dump(X_pca,open('X_pca-despues.pickle','w'))
    pickle.dump(svd,open('svd-despues.pickle','wb'))
    pickle.dump(pca,open('pca-despues.pickle','wb'))

    # Elijo mi clasificador.
    clf = RandomForestClassifier()

    # Ejecuto el clasificador entrenando con un esquema de cross validation
    # de 10 folds.
    res = cross_val_score(clf, X_svd, y, cv=10, n_jobs=-1)
    print "SVD-despues:", np.mean(res), np.std(res)
    res = cross_val_score(clf, X_pca, y, cv=10, n_jobs=-1)
    print "PCA-despues:", np.mean(res), np.std(res)

    ############


    X_svd = pd.DataFrame(X_train.todense())
    X_pca = pd.DataFrame(X_train.todense())
    extracted_features = processed_hams[0].keys()
    for extracted_feature in extracted_features: 
        print "Escribiendo feature " + extracted_feature
        X_svd[extracted_feature] = [mail[extracted_feature] for mail in (processed_hams+processed_spams)]
        X_pca[extracted_feature] = [mail[extracted_feature] for mail in (processed_hams+processed_spams)]

    ## SVD 
    svd = TruncatedSVD(n_components=100, random_state=42)
    X_svd_transformed = svd.fit_transform(X_svd)

    ## PCA
    pca = PCA(n_components=100, whiten=True)
    X_pca_transformed = pca.fit_transform(X_pca)

    pickle.dump(X_svd_transformed,open('X_svd-antes.pickle','w'))
    pickle.dump(X_pca_transformed,open('X_pca-antes.pickle','w'))
    pickle.dump(svd,open('svd-antes.pickle','wb'))
    pickle.dump(pca,open('pca-antes.pickle','wb'))

    # Elijo mi clasificador.
    clf = RandomForestClassifier()

    # Ejecuto el clasificador entrenando con un esquema de cross validation
    # de 10 folds.
    res = cross_val_score(clf, X_svd_transformed, y, cv=10, n_jobs=-1)
    print "SVD-antes:", np.mean(res), np.std(res)
    res = cross_val_score(clf, X_pca_transformed, y, cv=10, n_jobs=-1)
    print "PCA-antes:", np.mean(res), np.std(res)

