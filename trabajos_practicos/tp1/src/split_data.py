#40 % FOR testing (SPAM: 7585, HAM: )
#60 % FOR training (SPAM: 11379 , HAM:)

import json
import random

TRAINING_PERCENTAJE = 60

random.seed('tuvieja')
files = ['../data/spam_txt.json', '../data/ham_txt.json']
for _file in files:
	with open(_file,'r') as f:
		content = f.read()
	mails = json.loads(content)

	amount_of_training_mails = len(mails) * TRAINING_PERCENTAJE/100
	indexes_of_training_mails = random.sample(range(len(mails)), amount_of_training_mails)
	training_mails = [mails[index] for index in indexes_of_training_mails]
	testing_mails = [mails[index] for index in xrange(len(mails)) if index not in indexes_of_training_mails]

	with open("{}.training".format(_file),'w') as f:
		f.write(json.dumps(training_mails))

	with open("{}.testing".format(_file),'w') as f:
		f.write(json.dumps(testing_mails))








