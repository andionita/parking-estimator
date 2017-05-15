'''
Created on 11.05.2017

@author: andigenu
'''
import pandas as pd
import os
from collections import OrderedDict

d = []
record = {'C':123 , 'B': 234, 'A': 1}
d.append(record)
record = {'C':1231 , 'B': 2341, 'A': 11}
d.append(record)
result = pd.DataFrame(d)
result = result[['C','B','A']]

file = os.path.join(os.path.dirname(__file__), '../../sampledocs/SampleDataFrame.csv')
result.to_csv(file, sep=',', index=False)


    
