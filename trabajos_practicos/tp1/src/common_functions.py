from collections import defaultdict
import json
import email as email_parser
from emailHTMLParser import EmailHTMLParser
from text_tokenizer import *

def clean_string(string):
    return string.replace("\r","").replace("\n","").strip()

def parse_files(spam_filename, ham_filename):
    with open(spam_filename,'r') as f:
        spam_json = f.read()
    with open(ham_filename,'r') as f:
        ham_json = f.read()
    return json.loads(clean_string(spam_json)), json.loads(clean_string(ham_json))


def get_emails_by_ctype_to_payload(spam,ham):
    emails = [spam, ham]
    res = []
    for emails_of_type in emails:
        res_for_type = defaultdict(lambda:[],{})
        for i in xrange(len(emails_of_type)):
            msg = email_parser.message_from_string(emails_of_type[i].encode('ascii','ignore'))
            payload = msg.get_payload()
            contents = []
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
                res_for_type[content[0]].append(content[1])

        res.append(res_for_type)
    return {'spam':res[0], 'ham':res[1]}

def text_to_content_type(txt):
    return txt.replace("\n"," ").replace("\r"," ").split(' ')[0]

def content_types_for_email(email):
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

def text_from_email(email, separator='partugabylao'):
    contents = content_types_for_email(email)
    text_plain = contents['text/plain']
    html_content = contents['text/html']
    parser = EmailHTMLParser()
    html_text = []
    for html in html_content:
        parser.feed(html)
        if parser.data['body'] != '':
            html_text.append(parser.data['body'])
    text = (' ' + separator + ' ').join(text_plain + html_text)
    return ' '.join(tokenize(text))
