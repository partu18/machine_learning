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

def get_parsed_emails(filename):
    with open(filename,'r') as f:
        emails_json = f.read()
    return json.loads(clean_string(emails_json))


def features_extraction(filename):

    print "Leyendo json"
    emails = get_parsed_emails(filename)

    print "Preprocesando spams"
    preprocessed_emails = preprocess(emails)

    print "Extrayendo features de spam"
    processed_emails = [process_email(mail) for mail in preprocessed_emails] # Multiprocessing?

    print "Extrayendo textos para ngrams de spam"
    emails_text = [email[EMAIL_TEXT] for email in processed_emails]

    return processed_emails, emails_text