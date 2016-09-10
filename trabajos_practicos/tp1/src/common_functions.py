import json

from ngrams import find_ngrams
from math import log

def clean_string(string):
    return string.replace("\r","").replace("\n","").strip()

def parse_files(spam_filename, ham_filename):
    with open(spam_filename,'r') as f:
        spam_json = f.read()
    with open(ham_filename,'r') as f:
        ham_json = f.read()
    return json.loads(clean_string(spam_json)), json.loads(clean_string(ham_json))







##########  DEPREATED  ???  ###############################

def get_emails_by_ctype_to_payload(spam,ham):
    emails = [spam, ham]
    res = []
    for emails_of_type in emails:
        res_for_type = defaultdict(lambda:[],{})
        for i in xrange(len(emails_of_type)):
            msg = email_parser.message_from_string(emails_of_type[i].encode('ascii','ignore'))
            payload = msg.get_payload()
            contents = []
            if isinstance(payload,list):
                while len(payload) > 0:
                    part = payload.pop(0)
                    content = part.get_payload()
                    if isinstance(content,list):
                        payload = payload + content
                    else:
                        contents.append((text_to_content_type(part.get_content_type()),part.get_payload()))
            else:
                contents.append((text_to_content_type(msg.get_content_type()),payload))

            for content in contents:
                res_for_type[content[0]].append(content[1])

        res.append(res_for_type)
    return {'spam':res[0], 'ham':res[1]}

def idf(term,emails_as_ngrams,separator=None):
    # t must be in string, not array of strings
    #MAP REDUCE!!!!!!!!!!!!!!!
    D_t = len(filter(lambda x: term in x, emails_as_ngrams)) #[1 for ngrams_email in emails_as_ngrams if term in d])
    # D_size = float(len(emails_as_ngrams))
    D_size = float(emails_as_ngrams.size)
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

