#!/usr/bin/python
import sys,csv,math
sys.path.insert(1,'/usr/local/lib/python2.7/dist-packages/')
import sys, pickle, joblib

if __name__=="__main__":
    model_file_name = sys.argv[1]
    model_file = open(model_file_name,"r")
    model = pickle.load(model_file)
    model_file.close()
    print model.metadata
