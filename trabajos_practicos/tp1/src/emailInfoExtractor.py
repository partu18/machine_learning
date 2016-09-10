import email as email_parser
from emailHTMLParser import EmailHTMLParser
from collections import defaultdict
from constants import EMAIL_CTYPES, EMAIL_TEXT, EMAIL_HEADERS
from text_tokenizer import tokenize

def text_to_content_type(txt):
		    return txt.replace("\n"," ").replace("\r"," ").split(' ')[0]

class EmailInfoExtractor(object):
	@classmethod
	def get_email_info_structure(cls, email):
	    return {
	            EMAIL_CTYPES:cls.content_types_to_payload_from_email(email),
	            EMAIL_TEXT:cls.text_from_email(email),
	            EMAIL_HEADERS:cls.headers_from_email(email)
	            }

	@classmethod
	def text_from_email(cls, email, separator='partugabylao'):
	    contents = cls.content_types_to_payload_from_email(email)
	    text_plain = contents['text/plain']
	    html_text = []       
	    html_content = contents['text/html']
	    parser = EmailHTMLParser()
	    for html in html_content:
	        parser.feed(html)
	        if parser.data['body'] != '':
	            html_text.append(parser.data['body'])
	    text = (' ' + separator + ' ').join(text_plain + html_text)
	    return ' '.join(tokenize(text))

	@classmethod
	def content_types_to_payload_from_email(cls, email):
	    msg = email_parser.message_from_string(email.encode('ascii','ignore'))
	    payload = msg.get_payload()
	    contents = []
	    content_type_dict = defaultdict(lambda:[],{})
	    if isinstance(payload,list):
	        while len(payload) > 0:
	            part = payload.pop(0)
	            content = part.get_payload()
	            if isinstance(content,list):
	                payload = payload + content
	            else:
	                contents.append((text_to_content_type(part.get_content_type()),part.get_payload()))
	    else:
	        contents.append((text_to_content_type(msg.get_content_type()),payload))

	    for content in contents:
	        content_type_dict[content[0]].append(content[1])
	    return content_type_dict


	@classmethod
	def headers_from_email(cls, email):
		msg = email_parser.message_from_string(email.encode('ascii','ignore'))
		return {k.lower() for k,_ in dict(msg.items()).iteritems()}
		 
