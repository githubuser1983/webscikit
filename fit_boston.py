#!/usr/bin/python

import sys,csv,math, datetime
sys.path.insert(1,'/usr/local/lib/python2.7/dist-packages/')

from models import BostonModel
from sklearn.datasets import load_boston
from utils import save

# Load scikit's random forest classifier library
from sklearn.ensemble import RandomForestRegressor

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
clf = RandomForestRegressor(random_state=0)
clf.fit(df, y)

metadata = { 'version': 1,
             'created_at' : datetime.datetime.now(),
             'RFEstimator': clf }

bostonmodel = BostonModel(metadata)

print bostonmodel.metadata

print df.loc[0:2,:].to_json()

save(bostonmodel, "bostonmodel.pkl")
