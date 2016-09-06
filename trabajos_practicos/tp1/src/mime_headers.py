import email

from helper import Helper

def get_mime_headers_count(spam_emails, ham_emails):
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

    return headers_for_spam, headers_for_ham



def get_one_side_mime_headers(headers_for_spam, headers_for_ham, min_appeareances= 1):
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


def get_headers_that_make_the_difference(headers_for_spam, headers_for_ham, perc_difference=10):
    res = {}
    for header in headers_for_spam:
        if header in headers_for_ham.keys():
            amount_hams_with_header = headers_for_ham[header]
            amount_spams_with_header = headers_for_spam[header]
            if (min(amount_spams_with_header, amount_hams_with_header)*(100/perc_difference)) < max(amount_spams_with_header, amount_hams_with_header):
                res.update({header: (amount_spams_with_header, amount_hams_with_header)})
    return res



if __name__ == '__main__':
    helper = Helper()
    spam_emails, ham_emails = helper.get_parsed_emails()
    spam_headers, ham_headers = get_mime_headers_count(spam_emails, ham_emails)

    # print get_one_side_mime_headers(spam_headers, ham_headers, min_appeareances=100)
    print get_headers_that_make_the_difference(spam_headers, ham_headers, perc_difference=20)


