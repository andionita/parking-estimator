'''
Created on 04.05.2017

@author: andigenu
'''
import pandas as pd
from sklearn.preprocessing import LabelBinarizer

lb = LabelBinarizer()
X = lb.fit_transform([1, 2, 6, 4, 2])
pd.DataFrame(lb.transform([1, 6]), columns=lb.classes_).head()
print(lb.classes_)
print(lb.transform([1, 6]))
