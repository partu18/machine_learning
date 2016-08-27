import email
import json
from HTMLParser import HTMLParser
from collections import defaultdict

# create a subclass and override the handler methods
class EmailHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.data = defaultdict(lambda: 0,{})
        self.actual_tag = ''

    def handle_starttag(self, tag, attrs):
        tag = tag.replace('=','')
        self.actual_tag = tag
        if tag != 'body':
            self.data[tag] += 1

    def handle_data(self, content):
        if self.actual_tag == 'body':
            self.data['body'] = content


# class DataExtractor(object):

#     def __init__(self, spam_emails, ham_emails):
         # use parser to build a matrix with each value


class StatisticsGenerator(object):
    def __init__(self, spam_emails, ham_emails):
        self.SPAM = 'spam'
        self.HAM = 'ham'

        self.spam = spam_emails
        self.ham = ham_emails


    def print_stats(self, positive_spam, positive_ham, function_name):
        print "Function used: {}".format(function_name) 
        print 
        print "======SPAM======"
        print "Amount of positive spam emails: {}".format(positive_spam)
        print "Amount of negative spam emails: {}".format(len(self.spam) - positive_spam)
        print "Percentaje of positives: {}".format( float(positive_spam) / len(self.spam))
        print
        print "======HAM======"
        print "Amount of positive ham emails: {}".format(positive_ham)
        print "Amount of negative ham emails: {}".format(len(self.ham) - positive_ham)
        print "Percentaje of positives: {}".format( float(positive_ham) / len(self.ham))


    def get_stats_for_fn(self,function):
        """
            Function must be a function that returns either True (positive) or False (negative)
        """
        positive_spam = 0
        for mail in self.spam:
            positive_spam += 1 if function(mail) else 0

        positive_ham = 0
        for mail in self.ham:
            positive_ham += 1 if function(mail) else 0


        self.print_stats(positive_spam,positive_ham, function.func_name)

    def get_emails_by_ctype_to_payload(self):
        emails = [self.spam, self.ham]
        res = []
        for emails_of_type in emails:
            res_for_type = []
            non_parseable_emails = []
            for i in xrange(len(emails_of_type)):
                try:
                    msg = email.message_from_string(emails_of_type[i])
                except UnicodeEncodeError:
                    non_parseable_emails.append(i)
                    continue
                if msg.is_multipart():
                    mini_res = []
                    for payload in msg.get_payload():
                        mini_res.append({payload.get_content_type(): payload.get_payload()})
                    res_for_type.append(mini_res)
                else:
                    res_for_type.append([{msg.get_content_type(): msg.get_payload()}])
            res.append((res_for_type, non_parseable_emails))
        return {self.SPAM:res[0], self.HAM:res[1]}


def clean_string(string):
    return string.replace("\r","").replace("\n","").strip()

def has_html(email):
    return 'html' in email

def parse_files(spam_filename, ham_filename):
    with open(spam_filename,'r') as f:
        spam_json = f.read()

    with open(ham_filename,'r') as f:
        ham_json = f.read()

    return json.loads(clean_string(spam_json)), json.loads(clean_string(ham_json))


if __name__ == "__main__":
    spam_filename = 'spam_txt.json'
    ham_filename = 'ham_txt.json'

    spam_emails, ham_emails = parse_files(spam_filename, ham_filename)
    sg = StatisticsGenerator(spam_emails, ham_emails)

    res = sg.get_emails_by_ctype_to_payload()

    parser = EmailHTMLParser()

    txt = res['spam'][0][0][0]['text/html']

    parser.feed(clean_string(txt))

    #sg.get_stats_for_fn(has_html)