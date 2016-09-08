from collections import Counter
import json
from nltk.corpus import stopwords
from math import log
import numpy as np
import string

def clean_string(string):
    return string.replace("\r","").replace("\n","").strip()


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

def get_top_k_ngrams_count(emails_body, k, n=1, separator=None):
    #body_emails must be in plaint text
    n_gram_counter = Counter()
    for email_body in emails_body:
        n_grams = find_ngrams(email_body,n,separator=separator)
        for ng in n_grams:
           n_gram_counter[ng] += 1
    return n_gram_counter.most_common(k)

def get_top_percentile_ngrams_idf(emails_body, n=1, percentile=75, separator=None):
    #body_emails must be in plaint text
    idfs = dict()
    print "paso1"
    emails_as_ngrams = np.array([find_ngrams(e,n,separator=separator) for e in emails_body])
    print "paso2"
    n_grams = list(set([ng for ngs in emails_as_ngrams for ng in ngs]))
    print "paso3"
    idfs = {ng: idf(ng,emails_as_ngrams,separator=separator) for ng in n_grams}
    print "paso4"
    perc = np.percentile(idfs.values(), percentile)
    return {k: v for k, v in idfs.items() if v >= perc}

def get_bottom_percentile_ngrams_idf(emails_body, n=1, percentile=75, separator=None):
    #body_emails must be in plaint text
    idfs = dict()
    n_grams = [find_ngrams(e,n,separator=separator) for e in emails_body]
    n_grams = list(set([ng for ngs in n_grams for ng in ngs]))
    idfs = {ng: idf(ng,emails_body,separator=separator) for ng in n_grams}
    perc = np.percentile(idfs.values(), percentile)
    return {k: v for k, v in idfs.items() if v <= perc}

def get_top_percentile_different_count_ngrams(spam_emails, ham_emails, percentile=75, n=1, separator=None):
    spam_ngrams = [find_ngrams(e,n,separator=separator) for e in spam_emails]
    spam_ngrams = [ng for ngs in spam_ngrams for ng in ngs]
    spam_counter = {k: float(spam_ngrams.count(k)) for k in set(spam_ngrams)}

    ham_ngrams = [find_ngrams(e,n,separator=separator) for e in ham_emails]
    ham_ngrams = [ng for ngs in ham_ngrams for ng in ngs]
    ham_counter = {k: float(ham_ngrams.count(k)) for k in set(ham_ngrams)}

    ngram_counter = {k: (spam_counter[k] if k in spam_ngrams else 0, ham_counter[k] if k in ham_ngrams else 0) for k in list(set(spam_ngrams+ham_ngrams))}
    normalized_ngrams = {k: (v[0]/(v[0]+v[1]), v[1]/(v[0]+v[1])) for k, v in ngram_counter.items()}
    perc = np.percentile([abs(0.5-v[1]) for v in normalized_ngrams.values()], percentile)
    return {k: v for k, v in normalized_ngrams.items() if abs(0.5-v[1]) >= perc}


def idf(t,emails_as_ngrams,separator=None):
    # t must be in string, not array of strings
    print 'entro'
    #MAP REDUCE!!!!!!!!!!!!!!!
    D_t = len(filter(lambda x: t in x, emails_as_ngrams)) #[1 for d in emails_as_ngrams if t in d])
    print 'idf 2'
    # D_size = float(len(emails_as_ngrams))
    D_size = float(emails_as_ngrams.size)
    print 'idf 3'
    # D_t_size = float(len(D_t))
    D_t_size = float(D_t)
    return log( D_size / (1 + D_t_size))

def ft(t,d,separator=None):
    # t and d must be in strings, not arrays of strings
    n = len(t.split(' '))
    n_grams = find_ngrams(d, n, separator=separator)
    total_ngrams = float(len(n_grams))
    t_count = float(len([1 for _ in n_grams if n == t]))
    return  t_count / total_ngrams

def ft_idf(t,d,D):
    return ft(t,d)*idf(t,D)

def get_top_percentile_idf_touples(spam_emails,ham_emails, n=1, percentile=75, separator=None):
    idfs = dict()
    n_grams = [find_ngrams(e,n,separator=separator) for e in spam_emails+ham_emails]
    n_grams = list(set([ng for ngs in n_grams for ng in ngs]))
    idfs = {ng: (idf(ng,spam_emails,separator=separator),idf(ng,ham_emails,separator=separator)) for ng in n_grams}
    perc = np.percentile([abs(v[1]-v[0]) for v in idfs.values()], percentile)
    return {k: v for k, v in idfs.items() if abs(v[1]-v[0]) >= perc}
