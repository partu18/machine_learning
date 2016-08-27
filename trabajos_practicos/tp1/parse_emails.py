import email
import json


def emails_by_ctype_to_payload(emails):
    result = []
    non_parseable_emails = []
    # for ham_email in ham_emails:
    for i in xrange(len(emails)):
        try:
            msg = email.message_from_string(emails[i])
        except UnicodeEncodeError:
            non_parseable_emails.append(i)
            continue
        if msg.is_multipart():
            mini_res = []
            for payload in msg.get_payload():
                mini_res.append({payload.get_content_type(): payload.get_payload()})
            result.append(mini_res)
        else:
            result.append([{msg.get_content_type(): msg.get_payload()}])

    return result, non_parseable_emails

if __name__ == "__main__":
    ham_filename = 'ham_txt.json'
    spam_filename = 'spam_txt.json'

    with open(ham_filename,'r') as f:
        ham_json = f.read()

    with open(spam_filename,'r') as f:
        spam_json = f.read()

    ham_emails = json.loads(ham_json)
    spam_emails = json.loads(spam_json)

    parsed_emails, non_parseable_emails =  emails_by_ctype_to_payload(spam_emails)

    print parsed_emails[0]
    