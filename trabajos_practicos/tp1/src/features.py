from constants import EMAIL_CTYPES, EMAIL_HEADERS, EMAIL_ISMULTIPART

def is_multi_part(email_structure):
    #Spam 0.37, Ham 0.06
    return email_structure[EMAIL_ISMULTIPART]

def has_more_than_1_receiver(email_structure):
    #Spam 0.037, Ham 0.55
    receivers = email_structure[EMAIL_HEADERS].get('to')
    if receivers is None:
        receivers  = email_structure[EMAIL_HEADERS].get('reply-to','')  #FIXME
    return len(receivers.split(',')) > 1

# application -> o sea sin discriminar desp el tipo
def application_contents(email_structure):
    return sum([len(v) for k,v in email_structure[EMAIL_CTYPES].itermitems() if k.startswith('application')])

# text/html
def html_contents(email_structure):
    return len(email_structure[EMAIL_CTYPES].get('text/html',0))

# audio -> sin discriminar el tipo
def audio_contents(email_structure):
    return sum([len(v) for k,v in email_structure[EMAIL_CTYPES].itermitems() if k.startswith('audio')])

# image/gif
def gif_contents(email_structure):
    return len(email_structure[EMAIL_CTYPES].get('image/gif',0))

# image/jpeg
def jpeg_contents(email_structure):
    return len(email_structure[EMAIL_CTYPES].get('image/jpeg',0))

# text/plain
def plain_text_contents(email_structure):
    return len(email_structure[EMAIL_CTYPES].get('text/plain',0))

# imagenes globales -> O sea sin importar de que tipo
def image_contents(email_structure):
    return sum([len(v) for k,v in email_structure[EMAIL_CTYPES].itermitems() if k.startswith('image')])

def is_replay(email_structure):
    return 're:' in email_structure[EMAIL_HEADERS].get('subject','')

def has_javamail(email_structure):
    return 'javamail' in email_structure.get('message-id','')

