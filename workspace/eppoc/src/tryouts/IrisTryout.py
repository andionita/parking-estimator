'''
Created on 04.05.2017

@author: andigenu
'''
import numpy as np
from sklearn import datasets
iris = datasets.load_iris()
print(iris.data.dtype)
print(iris.target.dtype)
'''iris_X = iris.data
iris_y = iris.target
np.unique(iris_y)'''