'''
Created on 28.04.2017

@author: andigenu
'''
import numpy as np
from numpy import full

a = b = c = range(40, 1)
#print(list(a))
#print(list(zip(a,b,c)))

d = full((40, 1), 1)
print(d)
d[::4] += np.random.rand(10,1)
print(d)