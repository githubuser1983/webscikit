#!/usr/bin/python
import sys,csv,math
sys.path.insert(1,'/usr/local/lib/python2.7/dist-packages/')
import sys, pickle, joblib
from utils import load

if __name__=="__main__":
    model_file_name = sys.argv[1]
    model = load(model_file_name)
    print model.metadata
