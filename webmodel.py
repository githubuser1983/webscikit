import datetime, numpy as np

class WebModel(object):
    """
       Do not use this class directly as it does not do anything useful. Instead subclass it and override the methods transform() and predict()
       * metadata is a dictionary and can hold Estimators from Scikit-Learn, additional data as pandas.DataFrame, metrics about the model, version of model etc.
    """
    def __init__(self,metadata):
        self.metadata = metadata
        self.created_at = datetime.datetime.now()

    def predict(self,X):
        return np.ones(X.shape[0], dtype=int)

    def transform(self,X):
        return X

    def transform_predict(self,X):
        return self.predict(self.transform(X))
