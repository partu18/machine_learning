from constants import *

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
    return sum([len(v) for k,v in email_structure[EMAIL_CTYPES].iteritems() if k.startswith('application')])

# text/html
def html_contents(email_structure):
    return len(email_structure[EMAIL_CTYPES]['text/html'])

# audio -> sin discriminar el tipo
def audio_contents(email_structure):
    return sum([len(v) for k,v in email_structure[EMAIL_CTYPES].iteritems() if k.startswith('audio')])

# image/gif
def gif_contents(email_structure):
    return len(email_structure[EMAIL_CTYPES]['image/gif'])

# image/jpeg
def jpeg_contents(email_structure):
    return len(email_structure[EMAIL_CTYPES]['image/jpeg'])

# text/plain
def plain_text_contents(email_structure):
    return len(email_structure[EMAIL_CTYPES]['text/plain'])

# imagenes globales -> O sea sin importar de que tipo
def image_contents(email_structure):
    return sum([len(v) for k,v in email_structure[EMAIL_CTYPES].iteritems() if k.startswith('image')])

def is_replay(email_structure):
    return 're:' in email_structure[EMAIL_HEADERS].get('subject','')

def has_javamail(email_structure):
    return 'javamail' in email_structure.get('message-id','')

def text_length(email_structure):
    return len(email_structure[EMAIL_TEXT])

def spaces_count(email_structure):
    return email_structure[EMAIL_TEXT].count(' ')

def equals_count(email_structure):
    return email_structure[EMAIL_EQUAL_COUNT]

def star_count(email_structure):
    return email_structure[EMAIL_STAR_COUNT]
