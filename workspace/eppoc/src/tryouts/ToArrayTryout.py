'''
Created on 04.05.2017

@author: andigenu
'''
from sklearn.preprocessing import OneHotEncoder  
enc = OneHotEncoder()
X = [[0, 0, 3], [1, 1, 0], [0, 2, 1], [1, 0, 2]]
X_enc = enc.fit_transform(X)
print(X_enc)