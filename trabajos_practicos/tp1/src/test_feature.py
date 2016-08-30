import json
from features import *
from statisticsGenerator import StatisticsGenerator
from emailHTMLParser import EmailHTMLParser
from collections import Counter
#from nltk.corpus import stopwords
import operator

def clean_string(string):
    return string.replace("\r","").replace("\n","").replace("\t","  ").strip()


def parse_files(spam_filename, ham_filename):
    with open(spam_filename,'r') as f:
        spam_json = f.read()

    with open(ham_filename,'r') as f:
        ham_json = f.read()

    return json.loads(clean_string(spam_json)), json.loads(clean_string(ham_json))


if __name__ == "__main__":
    spam_filename = '../data/spam_train.json'
    ham_filename = '../data/ham_train.json'

    spam_emails, ham_emails = parse_files(spam_filename, ham_filename)
    sc = StatisticsGenerator(spam_emails, ham_emails)

    res = sc.get_emails_by_ctype_to_payload()
    
    parsed_spams = res['spam'][0]
    parsed_hams = res['ham'][0]

    #sc.get_stats_for_fn(has_more_than_10_to)

    ## Calculo de frecuencia de tags de html
    # spam_html_features = []
    # #summarization = Counter() # Calculo la aparicion global de las etiquetas HTML en spam
    # for mail in parsed_spams:
    #     parser = EmailHTMLParser()
    #     if mail.has_key('text/html'):
    #         for html in mail['text/html']:
    #             parser.feed(clean_string(html))
    #     #summarization += Counter(parser.data)
    #     spam_html_features.append(parser.data)


    ## Calculo de la frecuencia de palabras en los spam
    spam_text_data = []
    for mail in parsed_spams:
        if mail.has_key('text/plain'):
            spam_text_data += mail['text/plain']
    
    ## Usando TfidfVectorizer -> Muchas frecuencias repetidas, muy raro
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(max_df=0.6, stop_words='english')
    X = vectorizer.fit_transform(spam_text_data)
    idf = vectorizer.idf_
    frequencies_dict = dict(zip(vectorizer.get_feature_names(), idf))
    values = frequencies_dict.values()
    values.sort()
    perc = np.percentile(values,.75)
    filtered = {k: v for k, v in frequencies_dict.iteritems() if v > perc}
    
    # Usando el CountVectorizer -> Parece que no estamo asociando bien [palabra,conteo]
    from sklearn.feature_extraction.text import CountVectorizer
    count_vect = CountVectorizer(stop_words='english')
    Y = count_vect.fit_transform(spam_text_data)
    sum0 = Y.sum(0).A[0]
    frequencies_dict = {k:sum0[v] for k,v in count_vect.vocabulary_.iteritems()}
    sorted_freq = sorted(frequencies_dict.items(), key=operator.itemgetter(1))
    sorted_freq.reverse()


    ## Calculo de la frecuencia de palabras en los ham
    ham_text_data = []
    for mail in parsed_hams:
        if mail.has_key('text/plain'):
            ham_text_data += mail['text/plain']

    ## Usando TfidfVectorizer -> Muchas frecuencias repetidas, muy raro
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(max_df=0.6, stop_words='english') 
    X = vectorizer.fit_transform(ham_text_data)
    idf = vectorizer.idf_
    frequencies_dict = dict(zip(vectorizer.get_feature_names(), idf)) 
    values = frequencies_dict.values()
    values.sort()
    perc = np.percentile(values,.75)
    filtered = {k: v for k, v in frequencies_dict.iteritems() if v > perc}

    # Usando el CountVectorizer -> Parece que no estamo asociando bien [palabra,conteo]
    from sklearn.feature_extraction.text import CountVectorizer
    count_vect = CountVectorizer(stop_words='english')
    Y = count_vect.fit_transform(ham_text_data)
    sum0 = Y.sum(0).A[0]
    frequencies_dict = {k:sum0[v] for k,v in count_vect.vocabulary_.iteritems()}
    sorted_freq = sorted(frequencies_dict.items(), key=operator.itemgetter(1))
    sorted_freq.reverse()
