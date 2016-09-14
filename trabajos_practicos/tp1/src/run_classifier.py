## Imports de classifiers
import numpy as np
import pandas as pd
import pickle

from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.tree import DecisionTreeClassifier
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
def execute_classifier(classifier, X, target, params, n_jobs=1, folds=10, scoring='f1_weighted', grid_search=True, verbose=True): #definir scoring
    if grid_search:
        grid = GridSearchCV(classifier, params, cv=folds,n_jobs=n_jobs, scoring=scoring, verbose=verbose)
        grid.fit(X,target)
        print "Best Score:", grid.best_score_
        print "Best params:", grid.best_params_
        return grid.best_params_, grid.best_score_
    else:
        res = cross_val_score(classifier(**params), X, target, cv=folds, n_jobs=n_jobs, scoring=scoring, verbose=verbose)
        print "Mean: ", np.mean(res)
        print "Std: ", np.std(res)


print "Leyendo dataframe..."
df = pickle.load(open('df.pickle','r'))

extracted_features = list(df.columns)
extracted_features.remove('raw_email')
extracted_features.remove('class')

# Preparo data para clasificar
X = df[extracted_features].values
y = df['class']


### Example for CV
params = {'max_depth':150}
print "Comenzando a entrenar..."
execute_classifier(DecisionTreeClassifier,X,y,params,n_jobs=3, grid_search=False)

## Example for GridCV

###### If want to reduce dataset size for grid_search, do it here uncommenting the code below
# size = 50000
# X = df[extracted_features][0:size].values
# y = df['class'][0:size]
########

print "Ejecutando Grid Search..."
params = {'max_features':[50],'max_depth':[10,50,100,150]}
execute_classifier(DecisionTreeClassifier(),X,y,params,n_jobs=3, grid_search=True)
