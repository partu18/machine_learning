import email
from helper import Helper
from constants import SPAM, HAM

class MIMEHeadersCounter(object):
    def __init__(self, spam_emails, ham_emails):
        self.headers = {}
        self.count_MIME_headers(spam_emails, SPAM)
        self.count_MIME_headers(ham_emails, HAM)

    def unit_for_emails_type(self, _type):
        """
            Returns the correct tuple to add according to the _type of email      
        """
        if _type == SPAM:
            return (1,0)
        elif _type == HAM:
            return (0,1)
        else:
            raise Exception("Invalid type")

    def count_MIME_headers(self, emails, emails_type):
        unit = self.unit_for_emails_type(emails_type)
        for mail in emails:
            msg = email.message_from_string(mail.encode('ascii','ignore'))
            info = {k.lower():v for k,v in dict(msg.items()).iteritems()}
            for header in info.keys():
                if header in self.headers:
                    self.headers[header] = tuple(map(sum,(zip(self.headers[header],unit)))) #Gracias python!!   
                else:
                    self.headers[header] = unit


    def exclusive_one_side_headers(self, min_appeareances=1):
        """
            Returns headers that ONLY appear either in spam or ham emails, but not in both.
        """
        exclusive_headers = {}
        for header in self.headers:
            appearences = self.headers[header]
            if appearences.count(0) == 1 and max(appearences) > min_appeareances: #Truquillo
                exclusive_headers.update({header:self.headers[header]})
        return exclusive_headers


    def differencer_headers(self, perc_difference=50, min_appeareances= 0 ):
        """
            Returns headers that the difference between the appearences of each type is 
            greater than the perc_difference. Also, you can add a min_apparences threshold, which
            will be compared with the  minimum of the two apperances.
        """
        differencer_headers = {}
        for header in self.headers:
            appearences= self.headers[header]
            if ((min(appearences) + 1)* (100/float(perc_difference))) < max(appearences) and \
                min(appearences) > min_appeareances:
                differencer_headers.update({header:self.headers[header]})
        return differencer_headers


if __name__ == '__main__':
    helper = Helper()
    spam_emails, ham_emails = helper.get_parsed_emails()
    counter = MIMEHeadersCounter(spam_emails, ham_emails)
    print counter.exclusive_one_side_headers(min_appeareances=400)


