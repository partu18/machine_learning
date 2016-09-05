import json
class Helper(object):
    def __init__(self):
        self.spam_filename = '../data/spam_train.json'
        self.ham_filename = '../data/ham_train.json'


    def clean_string(self, string):
        return string.replace("\r","").replace("\n","").replace("\t","  ").strip()


    def get_parsed_emails(self):
        with open(self.spam_filename,'r') as f:
            spam_json = f.read()

        with open(self.ham_filename,'r') as f:
            ham_json = f.read()

        return json.loads(self.clean_string(spam_json)), json.loads(self.clean_string(ham_json))

