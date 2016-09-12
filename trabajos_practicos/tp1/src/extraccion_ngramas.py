from ngrams import *
import pickle
from common_functions import *
import json

text_hams = pickle.load(open('text_hams.pickle','r'))
text_spams = pickle.load(open('text_spams.pickle','r'))

for n in [1,2,3,4,5,7,10]:
	percentile = 0.005
	if n == 1:
		percentile = 0.5
	spam_bottom_idf = get_bottom_percentile_ngrams_idf(text_spams, n=n,percentile=percentile, separator='partugabylao')
	pickle.dump(dict(spam_bottom_idf),open('spam_bottom_'+`n`+'.pickle','w'))
	ham_bottom_idf = get_bottom_percentile_ngrams_idf(text_hams, n=n,percentile=percentile, separator='partugabylao')
	pickle.dump(dict(ham_bottom_idf),open('ham_bottom_'+`n`+'.pickle','w'))


for n in [1,2,3,4,5,7,10]:
	percentile = 0.005
	if n == 1:
		percentile = 0.5
	spam_bottom_idf = get_bottom_percentile_ngrams_idf(text_spams, n=n,percentile=percentile, separator='partugabylao')
	pickle.dump(dict(spam_bottom_idf),open('spam_bottom_'+`n`+'.pickle','w'))
	ham_bottom_idf = get_top_percentile_ngrams_idf(text_hams, n=n,percentile=100-percentile, separator='partugabylao')
	pickle.dump(dict(ham_bottom_idf),open('ham_bottom_'+`n`+'.pickle','w'))


for n in [1,2,3,4,5,7,10]:
	percentile = 0.005
	if n == 1:
		percentile = 0.5
	spam_bottom_idf = get_top_percentile_ngrams_idf(text_spams, n=n,percentile=100-percentile, separator='partugabylao')
	pickle.dump(dict(spam_bottom_idf),open('spam_bottom_'+`n`+'.pickle','w'))
	ham_bottom_idf = get_bottom_percentile_ngrams_idf(text_hams, n=n,percentile=percentile, separator='partugabylao')
	pickle.dump(dict(ham_bottom_idf),open('ham_bottom_'+`n`+'.pickle','w'))


for n in [1,2,3,4,5,7,10]:	
	spam = pickle.load(open('spam_bottom_'+`n`+'.pickle','r'))
	ham = pickle.load(open('ham_bottom_'+`n`+'.pickle','r'))

	res = light_touples(spam,ham,percentile=90)

	with open(`n`+'grams.json','w') as outputfile:
		json.dump(res.keys(),outputfile)
