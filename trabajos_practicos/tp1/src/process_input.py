from inspect import getmembers, isfunction
import features

features_functions = [m for m in getmembers(features) if isfunction(m[1])]

def process_email(email):
	return {name:extractor(email) for (name,extractor) in features_functions}
