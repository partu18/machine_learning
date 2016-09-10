import email
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

    def differencer_headers(self, times=1, min_appeareances= 0 ):
        """
            Returns headers which the difference between the greater and the lower appeareances is
            more than times*lower appearences . Also, you can add a min_apparences threshold, which
            will be compared with the  minimum of the two apperances.
        """
        differencer_headers = {}
        for header in self.headers:
            appearences= self.headers[header]
            if ((min(appearences) + 1)* times) < max(appearences) and \
                max(appearences) > min_appeareances:
                differencer_headers.update({header:self.headers[header]})
        return differencer_headers

    def get_headers_for_features(self):
        """ 
            Returns a set with the headers that must be extracted of each new email we 
            want to classify.
        """
        exclusive_headers = self.exclusive_one_side_headers(min_appeareances=100)
        differencer_headers = self.differencer_headers(times=4, min_appeareances=400)
        return set(exclusive_headers.keys()).union(set(differencer_headers))