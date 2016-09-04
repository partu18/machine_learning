import email

def has_html(mail):
    return 'html' in mail


def is_multi_part(mail):
    #25% de los spam
    #0% de los ham
    try:
        msg = email.message_from_string(mail)
        return msg.is_multipart()
    except UnicodeError:
        #Cannot be decoded
        return False

def has_more_than_10_to(mail):
    #CHOTO
    try:
        msg = email.message_from_string(mail)
        info = dict(msg.items())
        return len(info['to'].split(',')) > 10
    except UnicodeError:
        #Cannot be decoded
        return False
    except KeyError:
        return False


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
