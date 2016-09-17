## Imports de classifiers
import numpy as np
import pandas as pd
import pickle
import json
import sys

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
def execute_classifier(classifier, X, target, params, n_jobs=1, folds=10, scoring='accuracy', grid_search=True, verbose=True): #definir scoring
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

    if len(sys.argv) < 4:
        print 'usage {script_name} dataset parameters grid_output.pickle'.format(script_name=sys.argv[0])
        exit(1)

    clasificators = dict()
    clasificators['RandomForestClassifier'] = RandomForestClassifier
    
    print "Leyendo dataframe con reduccion de dimensionalidad..."
    X = pickle.load(open('pickles/'+sys.argv[1]+'_X.pisckle','r'))
    y = pickle.load(open('pickles/'+sys.argv[1]+'y.pickle','r'))

    print "Leyendo la grilla de parametros..."
    params = json.load(open('params/'+sys.argv[2]+'json','r'))
    
    print "Ejecutando Grid Search..."
    grid = execute_classifier(clasificators[sys.argv[3]], X, y, params, n_jobs=-1, grid_search=True)
    pickle.dump(grid,open('pickles/'+sys.argv[3],'wb'))
