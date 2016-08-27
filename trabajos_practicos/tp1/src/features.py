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

