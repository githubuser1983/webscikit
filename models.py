import sys,csv,math
sys.path.insert(1,'/usr/local/lib/python2.7/dist-packages/')
import pandas as pd

from webmodel import WebModel

class BostonModel(WebModel):
    def predict(self,data):
        rf = self.metadata["RFEstimator"]       
        prediction = rf.predict(data)
        return pd.DataFrame(prediction)


class IrisModel(WebModel):
    def predict(self,data):
        rf = self.metadata["RFClassifier"]       
        prediction = rf.predict(data)
        return pd.DataFrame(prediction)

    def transform(self,data):
        features = data.columns[:4]
        return data[features]

