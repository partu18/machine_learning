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

    # def handle_data(self, content):
    #     if self.actual_tag == 'body':
    #         self.data['body'] = content


# class DataExtractor(object):

#     def __init__(self, spam_emails, ham_emails):
         # use parser to build a matrix with each value

