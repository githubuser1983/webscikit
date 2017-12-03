
"""
This is an example model. Please do not locally import anything in this model, otherwise pickling will not work and your model can not be deployed.
Instead import from PYTHONPATH.
"""
import pandas as pd, cPickle as pickle, gzip

class BostonModel(object):
    """ Please do not change the class name"""

    def __init__(self,metadata):
        """ Do not change this method, as it initializes the instance with metadata"""
        if type(metadata) is dict:
            self.metadata = metadata
        else:
            raise TypeError("metadata must be of type dict, but is of type %s" % type(metadata))

    def predict(self,new_data):
        """ Please change this method. It will be called after self.transform(new_data) is called, so you can assume,
            that new_data is already transformed for prediction. You can also assume, that new_data is a pandas.DataFrame.
            If you need an Sklearn-Regressor / Classifier, please supply this when the model is instantiated with metadata:
                In fit_boston.py:
                       metadata = { 'mySkLearnRegressor' : myRandomForestRegressor, 
                                    'mySkLearnClassifier': myRandomForestClassifier,
                                    'someAdditionalDataFrameNeededForPrediction' : myDataFrame,
                                    'someConstant' : 3.14
                                  }
                       boston_model = BostonModel(metadata)
                Then you can access in this method with :
                        mySKLearnRegressor = self.metadata["mySKLearnRegressor"]
                        someConstant = self.metadata["someConstant"]
            Also make sure, that you convert your prediction to a pandas.DataFrame, as in this example
        """
        if not type(new_data) is pd.DataFrame:
            raise TypeError("new_data in predict must be of type pandas.DataFrame but is of type %s" % type(new_data))
        
        # start here implenting the prediction
        rf = self.metadata["mySkLearnRegressor"]       
        prediction = rf.predict(new_data)
        myConstant = self.metadata["someConstant"]
        new_prediction = myConstant * prediction + 2.0
        return pd.DataFrame(new_prediction)

    def transform(self,new_data):
        """ You can overwrite this method, if the new_data passed per POST as JSON needs to be transformed before one can
            call self.predict. By default, it returns new_data. If new_data is already transformed by the client issuing the POST request, than
            you might leave this method unchanged. If you need access to metadata, please read from self.metadata as in the self.predict method
        """
        if not type(new_data) is pd.DataFrame:
            raise TypeError("new_data in transform must be of type pandas.DataFrame but is of type %s" % type(new_data))
        # start here changing the method, if you want:
        return new_data

    def transform_predict(self,new_data):
        """ Do not change this method, as it will be called on the server when a POST request is issued by a client.
        """
        return self.predict(self.transform(new_data))


    def save(self):
        """Do not change this method.
           Save an object to a compressed disk file.
           Works well with huge objects.
        """
        model_name = self.__class__.__name__.replace("Model","").lower()
        filename = model_name + "_model.pkl"
        file = gzip.GzipFile(filename, 'wb')
        pickle.dump(self, file, -1)
        file.close()
