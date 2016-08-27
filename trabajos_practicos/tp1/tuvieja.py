import email
import json


if __name__ == "__main__":
    

    ham_filename = 'ham_txt.json'
    spam_filename = 'spam_txt.json'

    with open(ham_filename,'r') as f:
        ham_json = f.read()

    with open(spam_filename,'r') as f:
        spam_json = f.read()

    ham = json.loads(ham_json)
    spam = json.loads(spam_json)

    msg = email.message_from_string(spam[0])
    print msg.get_payload()[0]


