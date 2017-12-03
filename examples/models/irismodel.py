import sys,csv,math
sys.path.insert(1,'/usr/local/lib/python2.7/dist-packages/')
import pandas as pd, datetime


class IrisModel(object):
    def __init__(self,metadata):
        self.created_at = datetime.datetime.now()
        self.metadata = metadata

    def predict(self,data):
        rf = self.metadata["RFClassifier"]       
        prediction = rf.predict(data)
        return pd.DataFrame(prediction)

    def transform(self,data):
        features = data.columns[:4]
        return data[features]

