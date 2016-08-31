from HTMLParser import HTMLParser
from collections import defaultdict

# create a subclass and override the handler methods
class EmailHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = defaultdict(lambda: 0,{})
        self.inside_body = False

    def handle_starttag(self, tag, attrs):
        #tag = tag.replace('=','')
        if not tag.startswith('body'): #FIXME: ver si es prefijo de una etiqueta valida
            self.data[tag] += 1
        else:
            self.inside_body = True

    def handle_data(self, content):
        if self.inside_body:
            if self.data.has_key('body'):
                self.data['body'] += content
            else:
                self.data['body'] = content            

    def handle_endtag(self,tag):
        if tag.startswith('body'):
            self.inside_body = False

    def feed(self, data):
        self.data = defaultdict(lambda: 0,{})
        self.inside_body = False
        HTMLParser.feed(self,data)
