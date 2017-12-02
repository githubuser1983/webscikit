#!/usr/bin/python

import sys,csv,math, datetime
sys.path.insert(1,'/usr/local/lib/python2.7/dist-packages/')

from models import IrisModel
from sklearn.datasets import load_iris
from utils import save

# Load scikit's random forest classifier library
from sklearn.ensemble import RandomForestClassifier

# Load pandas
import pandas as pd

import pickle, joblib

# Load numpy
import numpy as np

# Set random seed
np.random.seed(0)

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
features = df.columns[:4]
y = pd.factorize(df['species'])[0]
clf = RandomForestClassifier(n_jobs=2, random_state=0)
clf.fit(df[features], y)

metadata = { 'version': 1,
             'created_at' : datetime.datetime.now(),
             'RFClassifier': clf }

irismodel = IrisModel(metadata)

print irismodel.metadata

print df.loc[0:2,:].to_json()

save(irismodel, "irismodel.pkl")
