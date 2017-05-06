'''
Created on 04.05.2017

@author: andigenu
'''
from sklearn.feature_extraction import DictVectorizer
v = DictVectorizer(sparse=False)

'''D = [{'foo': 1, 'bar': 2}, {'foo': 3, 'baz': 1}]
X = v.fit_transform(D)
print(X)
X = v.transform({'foo': 4, 'unseen_feature': 3})
print(X)'''



