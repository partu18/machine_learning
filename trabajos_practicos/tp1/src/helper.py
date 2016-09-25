import json
class Helper(object):
    def __init__(self):
        self.spam_train_filename = '../data/spam_train.json'
        self.ham_train_filename = '../data/ham_train.json'
        self.spam_test_filename = '../data/spam_test.json'
        self.ham_test_filename = '../data/ham_test.json'


    def clean_string(self, string):
        return string.replace("\r","").replace("\n","").replace("\t","  ").strip()


    def get_parsed_test_emails(self):
        with open(self.spam_test_filename,'r') as f:
            spam_json = f.read()

        with open(self.ham_test_filename,'r') as f:
            ham_json = f.read()

        return json.loads(self.clean_string(spam_json)), json.loads(self.clean_string(ham_json))


    def get_parsed_train_emails(self):
        with open(self.spam_train_filename,'r') as f:
            spam_json = f.read()

        with open(self.ham_train_filename,'r') as f:
            ham_json = f.read()

        return json.loads(self.clean_string(spam_json)), json.loads(self.clean_string(ham_json))

