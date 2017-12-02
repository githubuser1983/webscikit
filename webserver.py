#!/usr/bin/python
import sys,csv,math
sys.path.insert(1,'/usr/local/lib/python2.7/dist-packages/')

import json, pickle, datetime
from BaseHTTPServer import HTTPServer
from requesthandler import RequestHandler
from utils import load

def load_models(conf_file):
    models = dict([])
    cf = open(conf_file,"r")
    jsonstring = cf.read()
    urlmapping = json.loads(jsonstring)
    for url in urlmapping.keys():
        model_file = urlmapping[url]
        models[url] = (load(model_file),model_file)
    cf.close()
    return models

def runServerWithModels(models,server_class=HTTPServer, handler_class=RequestHandler, server_address=('',8000)):
    httpd = server_class(server_address, handler_class)
    httpd.models = models
    httpd.started_at = datetime.datetime.now()
    httpd.stats = dict([ (url,0) for url in models.keys() ])
    httpd.serve_forever()

if __name__ == '__main__':
    models = load_models("webscikit.conf")
    runServerWithModels(models)

   
