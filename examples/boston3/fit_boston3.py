#!/usr/bin/python
"""
This is an example python script to fit the model boston3.
Please do not import locally anything other than Boston3Model from boston3_model,
otherwise pickling will not work and you can not deploy the model.
"""
import sys, datetime
sys.path.insert(1,"/usr/local/lib/python2.7/dist-packages/")
from boston3_model import Boston3Model
from sklearn.datasets import load_boston

# Load scikit's random forest classifier library
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

# Load pandas
import pandas as pd

import pickle, joblib

# Load numpy
import numpy as np

# Set random seed
np.random.seed(0)

boston = load_boston()
df = pd.DataFrame(boston.data, columns=boston.feature_names)
y = boston.target
myRandomForestRegressor = RandomForestRegressor(random_state=0)
myRandomForestRegressor.fit(df, y)

myRandomForestClassifier = RandomForestClassifier(random_state=0)

myDataFrame = pd.DataFrame([1,2,3])

# please overwrite metadata with the data and regressors / classifiers you need to later transform, predict new data:

metadata = { 
             'version': 1,
             'created_at' : datetime.datetime.now(),
             'mySkLearnRegressor': myRandomForestRegressor,
             'mySkLearnClassifier' : myRandomForestClassifier,
             'someConstant' : 3.14,
             'someAdditionalDataFrameNeededForPrediction': myDataFrame
             }

# please do not change this part of the code:
boston3_model = Boston3Model(metadata)
boston3_model.save()
