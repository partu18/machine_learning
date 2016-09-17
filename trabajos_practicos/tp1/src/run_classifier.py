## Imports de classifiers
import numpy as np
import pandas as pd
import pickle
import json
import sys
from argparse import ArgumentParser

# clasificators
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import GridSearchCV

## Posibles scores: http://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
# accuracy
# average_precision
# f1
# f1_micro
# f1_macro
# f1_weighted
# f1_samples
# log_loss
# precision
# recall
# roc_auc
def execute_classifier(classifier, X, target, params, n_jobs=-1, folds=10, scoring='accuracy', grid_search=True, verbose=True): #definir scoring
    if grid_search:
        grid = GridSearchCV(classifier, params, cv=folds,n_jobs=n_jobs, scoring=scoring, verbose=verbose)
        grid.fit(X,target)
        print "Best Score:", grid.best_score_
        print "Best params:", grid.best_params_
        return grid
    else:
        res = cross_val_score(classifier(**params), X, target, cv=folds, n_jobs=n_jobs, scoring=scoring, verbose=verbose)
        print "Mean: ", np.mean(res)
        print "Std: ", np.std(res)

# Recibe 3 parametros: 
# 1) pickle del dataset a usar (PCA|LSA, features antes|despues)
# 2) json con la grilla de parametros a usar, mirar la carpeta params
# 3) nombre del pickle donde guardar el grid con los parametros optimos, lo guarda automaticamente en la carpeta pickles

if __name__ == '__main__':

    parser = ArgumentParser()

    parser.add_argument('-d',dest='dataset', help="Name of the dataset json file inside the pickles directory.")
    parser.add_argument('-p',dest='parameters', help="Name of the parameters json file inside the params directory.")
    parser.add_argument('-c',dest='classifier', choices=['RandomForest','KNN','Tree','NB','SVM'], help="Name of the classifier to use.")

    args = parser.parse_args()

    if not args.dataset or not args.parameters or not args.classifier:
        parser.error("Missing parameters")

    clasificators = dict()
    clasificators['RandomForest'] = RandomForestClassifier()
    clasificators['KNN'] = KNeighborsClassifier()
    clasificators['Tree'] = DecisionTreeClassifier()
    clasificators['NB'] = GaussianNB()
    clasificators['SVM'] = SVC()
    
    print "Leyendo dataframe con reduccion de dimensionalidad..."
    X = pickle.load(open('pickle/{}.pickle'.format(args.dataset),'r'))
    y = pickle.load(open('pickle/y.pickle','r'))

    print "Leyendo la grilla de parametros..."
    params = json.load(open('params/{}.json'.format(args.parameters),'r'))
    params = {k:map(lambda x: x if not(x == 'None') else None, v) for k,v in params.iteritems() }

    print "Ejecutando Grid Search..."
    grid = execute_classifier(clasificators[args.classifier], X, y, params, n_jobs=-1, grid_search=True)
    pickle.dump(grid,open('pickle/{}.pickle'.format(args.classifier+'_'+args.dataset),'wb'))
