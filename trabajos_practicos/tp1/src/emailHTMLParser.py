from HTMLParser import HTMLParser
from collections import defaultdict

# create a subclass and override the handler methods
class EmailHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = defaultdict(lambda: 0,{})
        self.inside_body = False
        self.valid_tags = ['a','abbr','address','area','article','aside','audio','b','base','bdi','bdo','blockquote','body','br','button','canvas','caption','cite','code','col','colgroup','data','datalist','dd','del','dfn','div','dl','dt','em','embed','fieldset','figcaption','figure','footer','form','h1','h2','h3','h4','h5','h6','head','header','hr','html','i','iframe','img','input','ins','kbd','keygen','label','legend','li','link','main','map','mark','meta','meter','nav','noscript','object','ol','optgroup','option','output','p','param','pre','progress','q','rb','rp','rt','rtc','ruby','s','samp','script','section','select','small','source','span','strong','style','sub','sup','table','tbody','td','template','textarea','tfoot','th','thead','time','title','tr','track','u','ul','var','video','wbr']

    def handle_starttag(self, tag, attrs):
        #tag = tag.replace('=','') # TODO: improve replacement? maybe: 
        # 1) replace 3d for '=' and 20 for ' ', and then split for spaces and check tag? this is for cases like 'a20href3d\"http:' that stands for a href=...
        # 2) use regex to replace every punctuation symbol for ''
        if (not tag.startswith('body')) and self.is_valid_tag(tag):
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
        self.data = defaultdict(lambda: 0,{'body':''})
        self.inside_body = False
        HTMLParser.feed(self,data)

    def is_valid_tag(self,tag):
        return tag in self.valid_tags