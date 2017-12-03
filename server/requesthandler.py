import sys
sys.path.insert(1,'/usr/local/lib/python2.7/dist-packages/')

from BaseHTTPServer import BaseHTTPRequestHandler
import logging, json
import pandas as pd, os, cPickle as pickle, gzip
from urlparse import parse_qs

def load(filename):
    """Loads a compressed object from disk
    """
    file = gzip.GzipFile(filename, 'rb')
    object = pickle.load(file)
    file.close()
    return object

class  RequestHandler(BaseHTTPRequestHandler): 

         
    def read_POST_data(self):
        content_length = int(self.headers['Content-Length']) # 
        post_data = self.rfile.read(content_length).decode("utf-8")
        return post_data

    def _set_headers(self,httpstatus=200):       
        self.send_response(httpstatus)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """ GET is reserved for "/stats" and "/loadModelAtURL?url=url10;model=model10.pkl"""
        if self.path == "/stats":
            resp = {'started_at':str(self.server.started_at)}
            for url in self.server.models.keys():
                model,filename = self.server.models[url]
                if not self.server.stats.has_key(url):
                    self.server.stats[url] = 0
                resp[url] = (self.server.stats[url],filename)
            response = json.dumps(resp)
            self._set_headers()
            self.wfile.write(response.encode("utf-8"))
            self.wfile.close()
        elif "/loadModelAtURL" in self.path:
            query = self.path.replace("/loadModelAtURL?","")
            params = parse_qs(query)
            print params
            url = params["url"][0]
            model_file = params["model"][0]
            model = load(os.path.join(self.server.webscikitmodelspath+"/",model_file))
            self.server.models[url] = (model,model_file)
            self._set_headers(200)
            self.wfile.close()
        else:
            # 404
            self.send_error(404)
            self.wfile.close()


    def do_POST(self):
        """ POST is reserved for doing only model predictions at urls defined in webscikit.conf"""
        model_found = False
        for url in self.server.models.keys():
            if self.path == url:
                self.server.stats[url] += 1
                model_found = True
                model,filename = self.server.models[url]
                data = self.read_POST_data()
                data = pd.read_json(data)
                prediction = model.transform_predict(data)
                json_prediction = prediction.to_json()
                response = json.dumps(json_prediction)
                self._set_headers()
                self.wfile.write(response.encode("utf-8"))
                self.wfile.close()
        if not model_found:
            # 404 model not found
            self.send_error(404)
            self.wfile.close()
