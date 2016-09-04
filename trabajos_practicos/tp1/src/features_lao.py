import json
from common_functions import *
from statisticsGenerator import StatisticsGenerator

def is_replay(msg):
    return 're:' in msg['subject']

def has_javamail(msg):
    return 'javamail' in info['message-id']

if __name__ == "__main__":
    spam_filename = '../data/spam_train.json'
    ham_filename = '../data/ham_train.json'

    spam_emails, ham_emails = parse_files(spam_filename, ham_filename)
    sc = StatisticsGenerator(spam_emails, ham_emails)

    emails = sc.get_emails_by_ctype_to_payload()

    ham_emails = emails['ham'][0]
    spam_emails = emails['spam'][0]

    print len([1 for e in ham_emails if has_javamail(e)])