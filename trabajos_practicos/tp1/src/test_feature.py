import json
from features import *
from statisticsGenerator import StatisticsGenerator
from emailHTMLParser import EmailHTMLParser
from collections import Counter

def clean_string(string):
    return string.replace("\r","").replace("\n","").strip()


def parse_files(spam_filename, ham_filename):
    with open(spam_filename,'r') as f:
        spam_json = f.read()

    with open(ham_filename,'r') as f:
        ham_json = f.read()

    return json.loads(clean_string(spam_json)), json.loads(clean_string(ham_json))



if __name__ == "__main__":
    spam_filename = '../data/spam_txt.json'
    ham_filename = '../data/ham_txt.json'

    spam_emails, ham_emails = parse_files(spam_filename, ham_filename)
    sc = StatisticsGenerator(spam_emails, ham_emails)

    res = sc.get_emails_by_ctype_to_payload()

    ham_html_features = []
    parsed_emails = res['ham'][0]
    # Calculo la aparicion global de las etiquetas HTML en spam
    summarization = Counter()
    for mail in parsed_emails:
        parser = EmailHTMLParser()
        if mail.has_key('text/html'):
            for html in mail['text/html']:
                parser.feed(clean_string(html))
        summarization += Counter(parser.data)
        ham_html_features.append(parser.data)



    #sc.get_stats_for_fn(has_more_than_10_to)
