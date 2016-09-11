#Type of emails 
SPAM = 'spam'
HAM = 'ham'

#Email info strcture
EMAIL_CTYPES = 'ctypes'
EMAIL_HEADERS = 'headers'
EMAIL_TEXT = 'text'
EMAIL_ISMULTIPART = 'ismultipart'

#Features
HEADERS_FEATURES = {'bcc', 'cc', 'content-class', 'delivery-notification', 'in-reply-to', 'location', 'original-recipient', 'precedence', 'priority', 'references', 'reply-to', 'return-path', 'thread-index', 'thread-topic', 'user-agent', 'x-antiabuse', 'x-antivirus', 'x-bcc', 'x-cc', 'x-commissioner-id', 'x-commissioner-league', 'x-egroups-return', 'x-env-sender', 'x-filename', 'x-from', 'x-ip', 'x-library', 'x-message-info', 'x-ms-has-attach', 'x-ms-tnef-correlator', 'x-msmail-priority', 'x-origin', 'x-originating-email', 'x-priority', 'x-server-uuid', 'x-source', 'x-source-args', 'x-source-dir', 'x-starscan-version', 'x-to', 'x-unsent', 'x-virus-scanned', 'x-wss-id'}
