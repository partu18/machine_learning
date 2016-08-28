from sklearn.cross_validation import train_test_split
import json
import pandas as pd

ham_txt= json.load(open('../data/ham_txt.json'))
spam_txt= json.load(open('../data/spam_txt.json'))

df = pd.DataFrame(ham_txt+spam_txt, columns=['text'])
df['class'] = ['ham' for _ in range(len(ham_txt))]+['spam' for _ in range(len(spam_txt))]

train, test = train_test_split(df, test_size=0.2, random_state=42)  

spam_train = train[train['class'] == 'spam']['text']
spam_test = test[test['class'] == 'spam']['text']
ham_train = train[train['class'] == 'ham']['text']
ham_test = test[test['class'] == 'ham']['text']

spam_test.to_json("../data/spam_test.json",orient='records')
spam_train.to_json("../data/spam_train.json",orient='records')
ham_test.to_json("../data/ham_test.json",orient='records')
ham_train.to_json("../data/ham_train.json",orient='records')