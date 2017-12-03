#!/usr/bin/python
import sys, os
sys.path.insert(1,'/usr/local/lib/python2.7/dist-packages/')

import json, datetime
from BaseHTTPServer import HTTPServer
from requesthandler import RequestHandler
import cPickle as pickle, gzip

def load(filename):
    """Loads a compressed object from disk
    """
    file = gzip.GzipFile(filename, 'rb')
    object = pickle.load(file)
    file.close()
    return object

def load_models(conf_file,webscikitmodelspath):
    models = dict([])
    cf = open(conf_file,"r")
    jsonstring = cf.read()
    urlmapping = json.loads(jsonstring)
    for url in urlmapping.keys():
        model_file = urlmapping[url]
        models[url] = (load(os.path.join(webscikitmodelspath+"/",model_file)),model_file)
    cf.close()
    return models

def runServerWithModels(models,server_class=HTTPServer, handler_class=RequestHandler, server_address=('',8000),webscikitmodelspath=None):
    httpd = server_class(server_address, handler_class)
    httpd.models = models
    httpd.started_at = datetime.datetime.now()
    httpd.stats = dict([ (url,0) for url in models.keys() ])
    httpd.webscikitmodelspath = webscikitmodelspath
    httpd.serve_forever()

if __name__ == '__main__':
    try:
        webscikitmodelspath = os.environ["WEBSCIKITMODELSPATH"]
    except KeyError:
        print "environment variable WEBSCIKITMODELSPATH is not set. Please set this path for example in ~/.bashrc and export it"
        sys.exit(-1)

    sys.path[0] = webscikitmodelspath

    models = load_models("webscikit.conf",webscikitmodelspath)
    runServerWithModels(models,webscikitmodelspath=webscikitmodelspath)

   
