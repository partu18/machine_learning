from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json

def clean_string(string):
    return string.replace("\r","").replace("\n","").strip()

def parse_files(spam_filename, ham_filename):
    with open(spam_filename,'r') as f:
        spam_json = f.read()
    with open(ham_filename,'r') as f:
        ham_json = f.read()
    return json.loads(clean_string(spam_json)), json.loads(clean_string(ham_json))

def get_idf_dict(emails, min_df=1, ngram_range=(1,1), stop_words='english'):
    vectorizer = TfidfVectorizer(min_df=min_df, ngram_range=ngram_range, stop_words=stop_words)
    X = vectorizer.fit_transform(emails)
    idf = vectorizer.idf_
    return dict(zip(vectorizer.get_feature_names(), idf))

def get_top_k_idf(spam_emails, ham_emails, k, min_df=1, n=1, stop_words='english'):
    ngram_range = (n,n)

    # obtaining the spam terms idf
    spam_idf_dict = get_idf_dict(spam_emails, min_df=min_df, ngram_range=ngram_range, stop_words=stop_words)

    spam_upper_perc = np.percentile(spam_idf_dict.values(),0)
    spam_lower_perc = np.percentile(spam_idf_dict.values(),100)
    spam_filtered_upper = {k: v for k, v in spam_idf_dict.iteritems() if v >= spam_upper_perc}
    spam_filtered_lower = {k: v for k, v in spam_idf_dict.iteritems() if v <= spam_lower_perc}
    # obtaining the ham terms idf
    ham_idf_dict = get_idf_dict(ham_emails, min_df=min_df, ngram_range=ngram_range, stop_words=stop_words)
    ham_upper_perc = np.percentile(ham_idf_dict.values(),0)
    ham_lower_perc = np.percentile(ham_idf_dict.values(),100)
    ham_filtered_upper = {k: v for k, v in ham_idf_dict.iteritems() if v >= ham_upper_perc}
    ham_filtered_lower = {k: v for k, v in ham_idf_dict.iteritems() if v <= ham_lower_perc}

    return spam_filtered_upper, spam_filtered_lower, ham_filtered_upper, ham_filtered_lower

# Ejemplo del get_top_k_idf
# spam_emails = ['house dog cake', 'house dog cat', 'house user car']
# ham_emails = ['yellow guitar bass', 'yellow guitar battery', 'yellow user car']
# k = 15
# a,b = get_top_k_idf(spam_email, ham_emails,k)
# a = { u'bass':    (inf, 1.6931471805599454),
#       u'battery': (inf, 1.6931471805599454),
#       u'cake':    (1.6931471805599454, inf),
#       u'car':     (1.6931471805599454, 1.6931471805599454),
#       u'cat':     (1.6931471805599454, inf),
#       u'dog':     (1.2876820724517808, inf),
#       u'guitar':  (inf, 1.2876820724517808),
#       u'house':   (1.0, inf),
#       u'user':    (1.6931471805599454, 1.6931471805599454),
#       u'yellow':  (inf, 1.0)}
#
#
# b = { u'bass':    (1.6931471805599454, inf),
#       u'battery': (1.6931471805599454, inf),
#       u'cake':    (inf, 1.6931471805599454),
#       u'car':     (1.6931471805599454, 1.6931471805599454),
#       u'cat':     (inf, 1.6931471805599454),
#       u'dog':     (inf, 1.2876820724517808),
#       u'guitar':  (1.2876820724517808, inf),
#       u'house':   (inf, 1.0),
#       u'user':    (1.6931471805599454, 1.6931471805599454),
#       u'yellow':  (1.0, inf)}






