from inspect import getmembers, isfunction
import features
import ngram_features

from common_functions import *

from helper import Helper

features_functions = [m for m in getmembers(features) if isfunction(m[1])]
ngram_features_functions = [m for m in getmembers(ngram_features) if isfunction(m[1])]

def preprocess(raw_emails):
	return [{'as_hash':get_emails_by_ctype_to_payload(mail),'text':text_from_email(mail)} for mail in emails] #TODO: multiprocessing?

def process_email(email):
	#simple features
	final_features = {name:extractor(email) for (name,extractor) in features_functions}
	for (name, extractor) in ngram_features_functions:
		ng_features = extractor(email)
		for feature_name,value in ng_features.iteritems():
			final_features[feature_name] = value
	return final_features

if __name__ == "__main__":

	helper = Helper()

	spam_emails, ham_emails = helper.get_parsed_emails()

	preprocessed_spams = preprocess(spam_emails)
	preprocessed_hams = preprocess(ham_emails)

