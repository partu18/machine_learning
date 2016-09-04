from collections import Counter
import json
from statisticsGenerator import StatisticsGenerator
from nltk.corpus import stopwords
from math import log

def clean_string(string):
    return string.replace("\r","").replace("\n","").strip()


def parse_files(spam_filename, ham_filename):
    with open(spam_filename,'r') as f:
        spam_json = f.read()
    with open(ham_filename,'r') as f:
        ham_json = f.read()
    return json.loads(clean_string(spam_json)), json.loads(clean_string(ham_json))




def find_ngrams(txt, n, remove_stopwords=False):
    blacklist = ['\t','\n','>','<','*','!','?']
    for item in blacklist:
        txt = txt.replace(item,'')
    txt = ' '.join(txt.split()) #para sacarle los multiples espacios
    words = txt.split(' ')
    if remove_stopwords:
        words = list(set(words) - set(stopwords.words('english')))
    return zip(*[words[i:] for i in range(n)])


def get_top_k_ngrams(emails_body, n, k):
    #body_emails must be in plaint text
    n_gram_counter = n_gram_counter()
    for email_body in emails_body:
        n_grams = find_ngrams(email_body, n)
        for n_gram in n_grams:
           n_gram_counter[n_gram] += 1
    return n_gram_counter.most_common(k)


def get_top_k_ngrams_freqs(emails_body, n, k):
    #body_emails must be in plaint text
    n_gram_counter = n_gram_counter()
    for email_body in emails_body:
        n_grams = find_ngrams(email_body, n)
        for n_gram in n_grams:
           n_gram_counter[n_gram] += 1
    return n_gram_counter.most_common(k)

def idf(t,D):
    n = len(t)
    total_documents = float(len(D))
    documents_with_t = float(len(filter(lambda x: t in find_ngrams(x, n), D)))
    return log( total_documents / (0.1 + documents_with_t))

def ft(t,d):
    ngrams = find_ngrams(d, len(t))
    total_ngrams = float(len(ngrams))
    total_ts = float(len(filter(lambda x: x == t, ngrams)))
    return  total_ts / total_ngrams

# toma un termino t (ngram), un documento d, la lista de todos los documentos D y calcula el ft-idf del ngram
# ejemplo: 
# t = ('a','b','c')
# d = 'a b c d e f g'
# D = ['a b c a b c','a b c d','d e f g t']
# ft_idf(t,d,D) -> 0.07133498878774648
# ya que la cantidad de apariciones de t en d es 1 y la cantidad de 3-grams en t son 5, la cantidad de documentos en D que contienen a t son 2
# por lo tanto ft_idf = ft * idf = 1/5 * log(3/(0.1+2))
# el termino 0.1 es para no dividir por 0 cuando el termino no esta en D.
def ft_idf(t,d,D):
    return ft(t,d)*idf(t,D)


if __name__ == "__main__":
    spam_filename = '../data/spam_train.json'
    ham_filename = '../data/ham_train.json'

    spam_emails, ham_emails = parse_files(spam_filename, ham_filename)
    sc = StatisticsGenerator(spam_emails, ham_emails)


    n = 3
    your_mommy = sc.get_emails_by_ctype_to_payload()


    ham_emails = your_mommy['ham'][0]
    spam_emails = your_mommy['spam'][0]

    plain_text_emails = [mail['text/plain'][0] for mail in ham_emails if 'text/plain' in mail.keys()]
    # plain_text_emails +=  [mail['text/plain'][0] for mail in spam_emails if 'text/plain' in mail.keys()]

    print get_top_k_ngrams(plain_text_emails, 3, 10)




