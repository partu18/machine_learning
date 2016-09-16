from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

text_hams = pickle.load(open('text_hams.pickle','r'))

text_spams = pickle.load(open('text_spams.pickle','r'))


all_texts = text_hams + text_spams


vectorizer = TfidfVectorizer(ngram_range=(1,3),stop_words='english',max_features=5000)

X_train = vectorizer.fit_transform(all_texts)

############

feature_names = vectorizer.get_feature_names()


means = np.mean(X_train,axis=0)

arr = np.squeeze(np.asarray(means))

features = zip(feature_names,arr)


sorted = sort_by_value(dict(features))

sorted.reverse()

##########

from sklearn.decomposition import TruncatedSVD

svd = TruncatedSVD(n_components=100, random_state=42)

res = svd.fit_transform(X_train)