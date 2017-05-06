'''
Created on 30.04.2017

@author: andigenu
'''
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

if __name__ == '__main__':
    digits = load_digits()
    X = digits.data
    y = digits.target
    
    # features are being scaled so that they may converge quicker
    pipeline = Pipeline([('ss', StandardScaler()), 
                         ('mlp', MLPClassifier(hidden_layer_sizes=(150,100), alpha=0.1))])
    print(cross_val_score(pipeline, X, y, n_jobs=-1))
    
