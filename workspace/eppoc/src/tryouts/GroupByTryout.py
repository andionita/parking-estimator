'''
Created on 15.05.2017

@author: andigenu
'''
import pandas as pd

result = pd.DataFrame([{"A":5, "X":1}, {"A":6, "X":2}, {"A":10, "X":3}, {"A":7, "X":2}, {"A":5, "X":3}])
#print(result)
#print(result["A"])
#print(result.groupby(["A"]).count())
print(result.loc[result["A"] == 5].as_matrix())