class StatisticsGenerator(object):
    def __init__(self, spam_emails, ham_emails):
        self.SPAM = 'spam'
        self.HAM = 'ham'

        self.spam = spam_emails
        self.ham = ham_emails

    def print_stats(self, positive_spam, positive_ham, function_name):
        print "Function used: {}".format(function_name) 
        print 
        print "======SPAM======"
        print "Amount of positive spam emails: {}".format(positive_spam)
        print "Amount of negative spam emails: {}".format(len(self.spam) - positive_spam)
        print "Percentaje of positives: {}".format( float(positive_spam) / len(self.spam))
        print
        print "======HAM======"
        print "Amount of positive ham emails: {}".format(positive_ham)
        print "Amount of negative ham emails: {}".format(len(self.ham) - positive_ham)
        print "Percentaje of positives: {}".format( float(positive_ham) / len(self.ham))


    def get_stats_for_fn(self,function):
        """
            Function must be a function that returns either True (positive) or False (negative)
        """
        positive_spam = 0
        fucked_emails = []
        for mail in self.spam:
            try:
                positive_spam += 1 if function(mail) else 0
            except Exception:  
                fucked_emails.append(self.spam.index(mail))
        positive_ham = 0
        for mail in self.ham:
            try:
                positive_ham += 1 if function(mail) else 0
            except Exception: 
                fucked_emails.append(self.ham.index(mail))

        print "Fucked emails {}".format(len(fucked_emails))
        self.print_stats(positive_spam,positive_ham, function.func_name)
