import email

from helper import Helper

def get_one_side_mime_headers(spam_emails, ham_emails, min_appeareances= 1):
    headers_for_spam = dict()
    for mail in spam_emails:
        msg = email.message_from_string(mail.encode('ascii','ignore'))
        info = {k.lower():v for k,v in dict(msg.items()).iteritems()}
        for header in info.keys():
            if header in headers_for_spam:
                headers_for_spam[header] += 1
            else:
                headers_for_spam[header] = 1

    headers_for_ham = dict()
    for mail in ham_emails:
        msg = email.message_from_string(mail.encode('ascii','ignore'))
        info = {k.lower():v for k,v in dict(msg.items()).iteritems()}
        for header in info.keys():
            if header in headers_for_ham:
                headers_for_ham[header] += 1
            else:
                headers_for_ham[header] = 1


    headers_only_spam =  set(headers_for_spam.keys()) - set(headers_for_ham.keys())
    headers_only_ham =  set(headers_for_ham.keys()) - set(headers_for_spam.keys())



    headers_only_spam_count = dict()
    for header in headers_only_spam:
        headers_only_spam_count[header] = headers_for_spam[header]

    headers_only_ham_count = dict()
    for header in headers_only_ham:
        headers_only_ham_count[header] = headers_for_ham[header]


    get_more_than_min_appeareaces = lambda x: x[1] > min_appeareances 
    return dict(filter(get_more_than_min_appeareaces, headers_only_spam_count.iteritems())), dict(filter(get_more_than_min_appeareaces, headers_only_ham_count.iteritems()))



if __name__ == '__main__':
    helper = Helper()
    spam_emails, ham_emails = helper.get_parsed_emails()
    print get_one_side_mime_headers(spam_emails, ham_emails, min_appeareances=100)


