'''
Created on 29.04.2017

@author: andigenu
Source: From Mastering Machine Learning with scikit-learn p.166
'''
from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics import f1_score, classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron

categories = ['rec.sport.hockey', 'rec.sport.baseball', 'rec.autos']
newsgroups_train = fetch_20newsgroups(subset='train', categories=categories, remove=('headers', 'footers', 'quotes'))
#print(newsgroups_train.keys())
#print(newsgroups_train.data[0])
#print(len(newsgroups_train.data))
#print(newsgroups_train.filenames)
#print(newsgroups_train.target_names)
#print(len(newsgroups_train.target))
#print(newsgroups_train.DESCR)
#print(newsgroups_train.description)

newsgroups_test = fetch_20newsgroups(subset='test', categories=categories, remove=('headers', 'footers', 'quotes'))
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(newsgroups_train.data)
X_test = vectorizer.transform(newsgroups_test.data)
classifier = Perceptron(n_iter=10, eta0=1)
classifier.fit_transform(X_train, newsgroups_train.target )
predictions = classifier.predict(X_test)
#print(confusion_matrix(newsgroups_test.target, predictions))
print(classification_report(newsgroups_test.target, predictions))
