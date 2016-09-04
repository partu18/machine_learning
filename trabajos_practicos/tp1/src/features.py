import email

def is_multi_part(mail):
    #Spam 0.37, Ham 0.06
    msg = email.message_from_string(mail.encode('ascii','ignore'))
    return msg.is_multipart()

def has_more_than_1_receiver(mail):
    #Spam 0.037, Ham 0.55
    try:
        msg = email.message_from_string(mail.encode('ascii','ignore'))
        info = {k.lower():v for k,v in dict(msg.items()).iteritems()}
        receivers = info.get('to', None)
        if receivers is None:
            receivers  = info['reply-to']            
        return len(receivers.split(',')) > 1
    except KeyError:
        raise Exception("fuck")

def has_reply_to(mail):
    #Spam 0.31, Ham, 0.05
    msg = email.message_from_string(mail.encode('ascii','ignore'))
    info = {k.lower():v for k,v in dict(msg.items()).iteritems()}
    return 'reply-to' in info.keys()



def content_types_in_mail(mail):
    msg = email.message_from_string(mail.encode('ascii','ignore'))
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

    return contents


# application -> o sea sin discriminar desp el tipo
def application_contents(mail):
    contents = content_types_in_mail(mail)
    return len([c for c in contents if c[0].startswith('application')])

# text/html
def html_contents(mail):
    contents = content_types_in_mail(mail)
    return len([ c for c in contents if c[0] == 'texto/html'])

# audio -> sin discriminar el tipo
def audio_contents(mail):
    contents = content_types_in_mail(mail)
    return len([ c for c in contents if c[0].startswith('audio')])

# image/gif
def gif_contents(mail):
    contents = content_types_in_mail(mail)
    return len([ c for c in contents if c[0] == 'image/gif'])

# image/jpeg
def jpeg_contens(mail):
    contents = content_types_in_mail(mail)
    return len([c for c in contents if c[0] == 'image/jpeg'])

# text/plain
def plain_text_contents(mail):
    contents = content_types_in_mail(mail)
    return len([c for c in contents if c[0] == 'text/plain'])

# imagenes globales -> O sea sin importar de que tipo
def image_contents(mail):
    contents = content_types_in_mail(mail)
    len([c for c in contents if c[0].startswith('image')])
