import email

def is_multi_part(mail):
    #Spam 0.37, Ham 0.06
    msg = email.message_from_string(mail.encode('ascii','ignore'))
    return msg.is_multipart()

def has_more_than_1_receiver(mail):
    #Spam 0.037, Ham 0.55
    msg = email.message_from_string(mail.encode('ascii','ignore'))
    info = {k.lower():v for k,v in dict(msg.items()).iteritems()}
    receivers = info.get('to', None)
    if receivers is None:
        receivers  = info.get('reply-to','')  #FIXME
    return len(receivers.split(',')) > 1

def has_reply_to(mail):
    #Spam 0.31, Ham, 0.05
    msg = email.message_from_string(mail.encode('ascii','ignore'))
    info = {k.lower():v for k,v in dict(msg.items()).iteritems()}
    return 'reply-to' in info.keys()

# application -> o sea sin discriminar desp el tipo
def application_contents(mail):
    return sum([len(v) for k,v in mail['as_hash'].itermitems() if k.startswith('application')])

# text/html
def html_contents(mail):
    return len(mail['as_hash']['text/html'])

# audio -> sin discriminar el tipo
def audio_contents(mail):
    return sum([len(v) for k,v in mail['as_hash'].itermitems() if k.startswith('audio')])

# image/gif
def gif_contents(mail):
    return len(mail['as_hash']['image/gif'])

# image/jpeg
def jpeg_contents(mail):
    return len(mail['as_hash']['image/jpeg'])

# text/plain
def plain_text_contents(mail):
    return len(mail['as_hash']['text/plain'])

# imagenes globales -> O sea sin importar de que tipo
def image_contents(mail):
    return sum([len(v) for k,v in mail['as_hash'].itermitems() if k.startswith('image')])

