import json
from features import *
from statisticsGenerator import StatisticsGenerator
from emailHTMLParser import EmailHTMLParser

def clean_string(string):
    return string.replace("\r","").replace("\n","").strip()


def parse_files(spam_filename, ham_filename):
    with open(spam_filename,'r') as f:
        spam_json = f.read()

    with open(ham_filename,'r') as f:
        ham_json = f.read()

    return json.loads(clean_string(spam_json)), json.loads(clean_string(ham_json))



if __name__ == "__main__":
    spam_filename = 'spam_txt.json'
    ham_filename = 'ham_txt.json'

    spam_emails, ham_emails = parse_files(spam_filename, ham_filename)
    sc = StatisticsGenerator(spam_emails, ham_emails)

    # res = sc.get_emails_by_ctype_to_payload()

    sc.get_stats_for_fn(has_more_than_10_to)


    parser = EmailHTMLParser()
    txt = res['spam'][0][0][0]['text/html']
    parser.feed(clean_string(txt))
