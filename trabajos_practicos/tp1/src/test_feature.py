from features import *
from statisticsGenerator import StatisticsGenerator
from helper import Helper
from emailHTMLParser import EmailHTMLParser
from collections import Counter
import numpy as numpy
from nltk.corpus import stopwords
import operator

if __name__ == "__main__":
    
    helper = Helper()
    spam_emails, ham_emails = helper.get_parsed_emails()
    sc = StatisticsGenerator(spam_emails, ham_emails)

    sc.get_stats_for_fn(has_reply_to)
#    
    # res = sc.get_emails_by_ctype_to_payload()
    # parsed_spams = res['spam']
    # parsed_hams = res['ham']



    # stop_words = stopwords.words('english')
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


    # Calculo de la frecuencia de palabras en los spam
    # spam_text_data = []
    # for mail in parsed_spams:
    #     if mail.has_key('text/plain'):
    #         spam_text_data += mail['text/plain']
        
    # spam_text_data = res['spam']['text/plain']

    ## Usando TfidfVectorizer -> Muchas frecuencias repetidas, muy raro
    # from sklearn.feature_extraction.text import TfidfVectorizer
    # vectorizer = TfidfVectorizer(stop_words=stop_words)
    # matrix = vectorizer.fit_transform(spam_text_data)
    # idf = vectorizer.idf_
    # frequencies_dict = dict(zip(vectorizer.get_feature_names(), idf))
    # values = frequencies_dict.values()
    # values.sort()
    # perc = np.percentile(values,.75)
    # filtered = {k: v for k, v in frequencies_dict.iteritems() if v > perc}
    
    # # Usando el CountVectorizer -> Parece que no estamo asociando bien [palabra,conteo]
    # from sklearn.feature_extraction.text import CountVectorizer
    # count_vect = CountVectorizer(stop_words=stop_words, min_df=0.1)
    # Y = count_vect.fit_transform(spam_text_data)
    # sum0 = Y.sum(0).A[0]
    # frequencies_dict = {k:sum0[v] for k,v in count_vect.vocabulary_.iteritems()}
    # sorted_freq = sorted(frequencies_dict.items(), key=operator.itemgetter(1))
    # sorted_freq.reverse()
