from collections import Counter
import json
from statisticsGenerator import StatisticsGenerator
from nltk.corpus import stopwords

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
    if(remove_stopwords)
        words = list(set(words) - set(stopwords.words('english')))
    return zip(*[words[i:] for i in range(n)])


def get_top_10_ngrams(emails_body, n):
    #body_emails must be in plaint text
    n_gram_counter = Counter()
    for email_body in emails_body:
        n_grams = find_ngrams(email_body, n)
        for n_gram in n_grams:
           n_gram_counter[n_gram] += 1
    return n_gram_counter.most_common(10)



if __name__ == "__main__":
    spam_filename = '../data/spam_train.json'
    ham_filename = '../data/ham_train.json'

    spam_emails, ham_emails = parse_files(spam_filename, ham_filename)
    sc = StatisticsGenerator(spam_emails, ham_emails)


    n = 3
    your_mommy = sc.get_emails_by_ctype_to_payload()


    ham_emails = your_mommy['ham'][0]
    spam_emails = your_mommy['spam'][0]

    plain_text_emails =  [mail['text/plain'][0] for mail in ham_emails if 'text/plain' in mail.keys()]
    # plain_text_emails +=  [mail['text/plain'][0] for mail in spam_emails if 'text/plain' in mail.keys()]

    print    get_top_10_ngrams(plain_text_emails, 3)




