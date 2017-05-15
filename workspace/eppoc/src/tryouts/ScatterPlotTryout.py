'''
Created on 15.05.2017

@author: andigenu
'''
import matplotlib.pyplot as plt
import random
import numpy

value_range = 1000
n_samples = 1000
y = random.sample(range(value_range), n_samples)
plt.scatter(range(n_samples), y[:1000], s=1)
plt.xlabel('Values')
plt.ylabel('Points')
plt.show()
