from collections import Counter
import json
from nltk.corpus import stopwords
from math import log
import numpy as np
import string
from collections import defaultdict

def clean_string(string):
    return string.replace("\r","").replace("\n","").strip()

def sort_by_value(dict):
    import operator
    return sorted(dict.items(), key=operator.itemgetter(1))

def parse_files(spam_filename, ham_filename):
    with open(spam_filename,'r') as f:
        spam_json = f.read()
    with open(ham_filename,'r') as f:
        ham_json = f.read()
    return json.loads(clean_string(spam_json)), json.loads(clean_string(ham_json))


def find_ngrams(txt, n, remove_stopwords=False, separator=None):
    blacklist = '\t\n' + string.punctuation
    for item in blacklist:
        txt = txt.replace(item,'')
    txt = ' '.join(txt.split()) #para sacarle los multiples espacios
    words = txt.split(' ')
    if remove_stopwords:
        words = list(set(words) - set(stopwords.words('english')))
    ngrams = zip(*[words[i:] for i in range(n)])
    if separator != None:
        ngrams = [ng for ng in ngrams if not(separator in ng)]
    return [' '.join(ngram) for ngram in ngrams]

def get_top_k_ngrams_count(lemmatized_emails, k, n=1, separator=None):
    #body_emails must be in plain text
    n_gram_counter = Counter()
    for email_body in lemmatized_emails:
        n_grams = find_ngrams(email_body,n,separator=separator)
        for ng in n_grams:
           n_gram_counter[ng] += 1
    return n_gram_counter.most_common(k)

# tdf stands for term document frecuency which is the total of document from the document array that contains the term
# idf stands for inverse document frequency, defined as idf(t,D) = |D|/|{d in D where t in d}|
# other_ngrams list allows to calculate idf for ngrams that doesn't appear in anny document
def get_ngrams_idf(lemmatized_emails, n=1, separator=None, percentile=25):
    tdfs = defaultdict(lambda:0,{})
    emails_as_ngrams = [find_ngrams(e,n,separator=separator) for e in lemmatized_emails]
    for ngrams_for_email in emails_as_ngrams:
        for ng in set(ngrams_for_email):
            tdfs[ng] += 1
    items = tdfs.items()
    count_ngrams = len(emails_as_ngrams)
    return {k: log(float(count_ngrams)/float(1+v)) for k, v in items}

def get_ngrams_idf_edges(lemmatized_emails,n=1, percentile=25,separator=None):
    tdfs = defaultdict(lambda:0,{})
    emails_as_ngrams = [find_ngrams(e,n,separator=separator) for e in lemmatized_emails]
    for ngrams_for_email in emails_as_ngrams:
        for ng in set(ngrams_for_email):
            tdfs[ng] += 1
    tdfs_values = tdfs.values()
    tdfs_items = tdfs.items()
    lower_perc = np.percentile(tdfs_values, percentile)
    upper_perc = np.percentile(tdfs_values, 100 - percentile)
    tdfs = {k: v for k, v in tdfs_items if v < lower_perc or v > upper_perc}
    items = tdfs.items()
    count_ngrams = len(emails_as_ngrams)
    return {k: log(float(count_ngrams)/float(1+v)) for k, v in items}    


def get_top_percentile_ngrams_idf(lemmatized_emails, n=1, percentile=75, separator=None):
    #body_emails must be in plain text
    idfs = get_ngrams_idf(lemmatized_emails,n,separator=separator)
    perc = np.percentile(idfs.values(), percentile)
    return {k: v for k, v in idfs.items() if v > perc}

def get_bottom_percentile_ngrams_idf(lemmatized_emails, n=1, percentile=75, separator=None):
    #body_emails must be in plain text
    idfs = get_ngrams_idf(lemmatized_emails,n,separator=separator)
    perc = np.percentile(idfs.values(), percentile)
    return {k: v for k, v in idfs.items() if v < perc}

def get_top_percentile_different_count_ngrams(lemmatized_spam_emails, lemmatized_ham_emails, n=1, percentile=75, separator=None):
    spam_ngrams = [find_ngrams(e,n,separator=separator) for e in lemmatized_spam_emails]
    spam_ngrams = [ng for ngs in spam_ngrams for ng in ngs]
    spam_counter = {k: float(spam_ngrams.count(k)) for k in set(spam_ngrams)}

    ham_ngrams = [find_ngrams(e,n,separator=separator) for e in lemmatized_ham_emails]
    ham_ngrams = [ng for ngs in ham_ngrams for ng in ngs]
    ham_counter = {k: float(ham_ngrams.count(k)) for k in set(ham_ngrams)}

    ngram_counter = {k: (spam_counter[k] if k in spam_ngrams else 0, ham_counter[k] if k in ham_ngrams else 0) for k in list(set(spam_ngrams+ham_ngrams))}
    normalized_ngrams = {k: (v[0]/(v[0]+v[1]), v[1]/(v[0]+v[1])) for k, v in ngram_counter.items()}
    perc = np.percentile([abs(0.5-v[1]) for v in normalized_ngrams.values()], percentile)
    return {k: v for k, v in normalized_ngrams.items() if abs(0.5-v[1]) > perc}

def get_top_percentile_idf_touples(lemmatized_spam_emails,lemmatized_ham_emails, n=1, percentile=75, separator=None):
    print "Calculando ngrams spam"
    spam_emails_as_ngrams = [find_ngrams(e,n,separator=separator) for e in lemmatized_spam_emails]
    print "Calculando ngrams ham"
    ham_emails_as_ngrams = [find_ngrams(e,n,separator=separator) for e in lemmatized_ham_emails]
    #idfs_spam = get_ngrams_idf(lemmatized_spam_emails,n,set(sum(ham_emails_as_ngrams,[]))-set(sum(spam_emails_as_ngrams,[])),separator=separator)
    #idfs_ham = get_ngrams_idf(lemmatized_ham_emails,n,set(sum(spam_emails_as_ngrams,[]))-set(sum(ham_emails_as_ngrams,[])),separator=separator)
    print "Calculando IDFs spam"
    idfs_spam = get_ngrams_idf(lemmatized_spam_emails,n,set(sum(ham_emails_as_ngrams,[]))-set(sum(spam_emails_as_ngrams,[])),percentile=percentile,separator=separator)
    print "Calculando IDFs ham"
    idfs_ham = get_ngrams_idf(lemmatized_ham_emails,n,set(sum(spam_emails_as_ngrams,[]))-set(sum(ham_emails_as_ngrams,[])),percentile=percentile,separator=separator)
    #idfs = {k:(idfs_spam[k],idfs_ham[k]) for k in idfs_ham.keys() } # Las keys de idfs_ham y de idfs_spam son las mismas :) (no?)
    print "zipeando"
    idfs = dict(zip(idfs_spam.keys(),(idfs_spam.values(),idfs_ham.values())))
    print "percentileando"
    perc = np.percentile([abs(v[1]-v[0]) for v in idfs.values()], percentile)
    print "por retornar"
    return {k: v for k, v in idfs.items() if abs(v[1]-v[0]) > perc}


def light_touples(spam_ngram_idf, ham_ngram_idf, percentile=0):
    inter = set(spam_ngram_idf.keys()).intersection(ham_ngram_idf.keys())
    union = set(spam_ngram_idf.keys()).union(ham_ngram_idf.keys())
    touples = {k: ((spam_ngram_idf[k],ham_ngram_idf[k]) if k in inter else ((spam_ngram_idf[k],float('Inf')) if k in spam_ngram_idf.keys() else (float('Inf'),ham_ngram_idf[k]) ))  for k in union }
    abs_diff = {k:(abs(v[0]-v[1])) for k,v in touples.iteritems()}
    return dict(sort_by_value(abs_diff))

