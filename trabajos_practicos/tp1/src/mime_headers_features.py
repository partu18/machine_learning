from constants import HEADERS_FEATURES, EMAIL_HEADERS

def is_mime_header_present(email_structure):
	res = {}
	headers_in_email = email_structure[EMAIL_HEADERS].keys() 
	for header in HEADERS_FEATURES:
		key = "is_header_mime_{}_present".format(header)
		value = header in headers_in_email
		res.update({key:value})
	return res


	 