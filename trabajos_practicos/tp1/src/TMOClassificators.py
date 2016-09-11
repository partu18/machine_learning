import time

from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from collections import namedtuple

PredictionInfo = namedtuple("PredictionInfo", "prediction time_invested score")


class TMOClassificators(object):
    """
        The Mother Of Classificators, will make all tasks (fitting, predicting, etc) with all the classifiers configured.
    """

    def __init__(self, data, target, classifiers= None, **kwargs):
        """
            You can provide with the configuration you want the internal classifiers or provide external classifiers (already instantiated).
            
            Doc: - http://scikit-learn.org/stable/modules/naive_bayes.html
                 - http://scikit-learn.org/stable/modules/neighbors.html
                 - http://scikit-learn.org/stable/modules/svm.html
                 - http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
        """
        self.data = data    
        self.target = target
        self.predictions_info = {}
        self._classifiers = classifiers or [ GaussianNB(**kwargs),
                                             MultinomialNB(**kwargs),
                                             KNeighborsClassifier(**kwargs),
                                             RadiusNeighborsClassifier(**kwargs),
                                             SVC(**kwargs),
                                             NuSVC(**kwargs),
                                             LinearSVC(**kwargs),
                                             RandomForestClassifier(**kwargs)    
                                           ]
    def name(self, classifier):
        return [_classifier.__class__.__name__ for _classifier in self._classifiers if _classifier == classifier][0]


    def calculate_score(self):
        for _classifier in self._classifiers:
            score = _classifier.score(self.data, self.target)
            print score
            old_prediction_info = self.predictions_info[self.name(_classifier)] 
            new_prediction_info = PredictionInfo(old_prediction_info.prediction, old_prediction_info.time_invested, score)  
            self.predictions_info[self.name(_classifier)] =  new_prediction_info


    def predict(self):
        for _classifier in self._classifiers:
            start_time = time.time()
            prediction = _classifier.predict(self.data)
            end_time = time.time()
            prediction_info = PredictionInfo(prediction, end_time - start_time, -1)
            self.predictions_info.update({self.name(_classifier):prediction_info})

    def fit(self):
        for _classifier in self._classifiers:
            _classifier.fit(self.data, self.target)

    def get_prediction_difference(self):
        output_template = """<{classifier}>
\t Number of bad-predicted points: {bad_predicted}/{total}.
\t Time invested(s) in prediction: {time}.
\t Score of prediction: {score}

"""
        
        for _classifier in self._classifiers:
            classifier_name = self.name(_classifier)
            prediction = self.predictions_info.get(classifier_name).prediction
            time_invested_in_prediction = self.predictions_info.get(classifier_name).time_invested
            bad_predicted = (self.target != prediction).sum()
            score = self.predictions_info.get(classifier_name).score
            print output_template.format( classifier = classifier_name,
                                    total = len(self.target),
                                    bad_predicted = bad_predicted,
                                    time = time_invested_in_prediction,
                                    score = score
                                  )