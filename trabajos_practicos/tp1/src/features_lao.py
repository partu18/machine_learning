import json
import email
import pandas as pd

def clean_string(string):
    return string.replace("\r","").replace("\n","").strip()


def parse_files(spam_filename, ham_filename):
    with open(spam_filename,'r') as f:
        spam_json = f.read()

    with open(ham_filename,'r') as f:
        ham_json = f.read()

    return json.loads(clean_string(spam_json)), json.loads(clean_string(ham_json))

def is_replay(msg):
    try:
        info = dict(email.message_from_string(msg).items())
        return 're:' in info['subject']
    except UnicodeError:
        #Cannot be decoded
        return False
    except KeyError:
        return False

def has_javamail(msg):
    try:
        info = dict(email.message_from_string(msg).items())
        return 'javamail' in info['message-id']
    except UnicodeError:
        #Cannot be decoded
        return False
    except KeyError:
        return False

ham_emails = json.load(open('../data/ham_train.json'))
spam_emails = json.load(open('../data/spam_train.json'))

df = pd.DataFrame(ham_emails+spam_emails, columns=['text'])
df['class'] = ['ham' for _ in range(len(ham_emails))]+['spam' for _ in range(len(spam_emails))]

# desde aca es solo codigo para contar repeticiones y ver si tenian sentido las features
df['je'] = [has_javamail(r[1]['text']) for r in df.iterrows()]

print len(df[df['class'] == 'spam'][df['je'] == True]), len(df[df['class'] == 'ham'][df['je'] == True])