# general purpose
import json

# features
import features.mime_headers_features as mime_headers_features
import features.multiples_features as features

# Text processing
from inspect import getmembers, isfunction
from emailInfoExtractor import *

mime_headers_features_functions = [m for m in getmembers(mime_headers_features) if isfunction(m[1])]
features_functions = [m for m in getmembers(features) if isfunction(m[1])]

def preprocess(raw_emails):
    return [get_email_info_structure(mail) for mail in raw_emails]

def process_email(email):
    # Simple features
    final_features = {name:extractor(email) for (name,extractor) in features_functions}

    # Mime features
    for (name, extractor) in mime_headers_features_functions:
        header_features = extractor(email)
        for feature_name,value in header_features.iteritems():
            final_features[feature_name] = value        

    return final_features

def clean_string(self, string):
        return string.replace("\r","").replace("\n","").replace("\t","  ").strip()

def get_parsed_emails(spam_filename, ham_filename):
    with open(spam_filename,'r') as f:
        spam_json = f.read()

    with open(ham_filename,'r') as f:
        ham_json = f.read()

    return json.loads(clean_string(spam_json)), json.loads(clean_string(ham_json))

def features_extraction(spam_filename, ham_filename):

    print "Leyendo jsons"
    spam_emails, ham_emails = get_parsed_emails(spam_filename, ham_filename)

    print "Preprocesando spams"
    preprocessed_spams = preprocess(spam_emails)
    print "Preprocesando hams"
    preprocessed_hams = preprocess(ham_emails)

    print "Extrayendo features de spam"
    processed_spams = [process_email(mail) for mail in preprocessed_spams] # Multiprocessing?
    print "Extrayendo features de ham"
    processed_hams = [process_email(mail) for mail in preprocessed_hams] # Multiprocessing?

    print "Extrayendo textos para ngrams de spam"
    text_hams = [email[EMAIL_TEXT] for email in preprocessed_hams]
    print "Extrayendo textos para ngrams de ham"
    text_spams = [email[EMAIL_TEXT] for email in preprocessed_spams]

    return processed_hams, processed_spams, text_hams, text_spams