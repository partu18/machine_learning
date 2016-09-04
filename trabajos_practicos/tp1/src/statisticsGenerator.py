import email
from collections import defaultdict

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
            res_for_type = defaultdict(lambda:[],{})
            for i in xrange(len(emails_of_type)):
                msg = email.message_from_string(emails_of_type[i].encode('ascii','ignore'))
                payload = msg.get_payload()
                contents = []
                if isinstance(payload,list):
                    while len(payload) > 0:
                        part = payload.pop(0)
                        content = part.get_payload()
                        if isinstance(content,list):
                            payload = payload + content
                        else:
                            contents.append((self.text_to_content_type(part.get_content_type()),part.get_payload()))
                else:
                    contents.append((self.text_to_content_type(msg.get_content_type()),payload))

                for content in contents:
                    res_for_type[content[0]].append(content[1])

            res.append(res_for_type)
        return {self.SPAM:res[0], self.HAM:res[1]}

    def text_to_content_type(self,txt):
        return txt.replace("\n"," ").replace("\r"," ").split(' ')[0]
