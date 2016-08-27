import json
from features import *
from spamClasifier import SpamClasifier


def parse_files(spam_filename, ham_filename):
    with open(spam_filename,'r') as f:
        spam_json = f.read()

    with open(ham_filename,'r') as f:
        ham_json = f.read()

    return json.loads(spam_json), json.loads(ham_json) 



if __name__ == "__main__":
    spam_filename = 'spam_txt.json'
    ham_filename = 'ham_txt.json'

    spam_emails, ham_emails = parse_files(spam_filename, ham_filename)
    sc = SpamClasifier(spam_emails, ham_emails)

    # res = sc.get_emails_by_ctype_to_payload()

    sc.get_stats_for_fn(has_more_than_10_to)