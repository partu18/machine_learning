import json 

def is_prefix(ngram,ngram_list):
	return len([ng for ng in ngram_list if ng.startswith(ngram) and len(ng) > len(ngram)]) > 0

ngrams = []
existent_ngrams = [1,2,3,4,5,7,10]
for i in xrange(len(existent_ngrams)):
	ngrams = ngrams + json.load(open('ngram_features/'+str(existent_ngrams[i])+'grams.json'))

prefixes = [ng for ng in ngrams if is_prefix(ng,ngrams)]

filtered = [ng for ng in ngrams if not(is_prefix(ng,ngrams))]