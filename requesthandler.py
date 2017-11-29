import sys,csv,math
sys.path.insert(1,'/usr/local/lib/python2.7/dist-packages/')

from BaseHTTPServer import BaseHTTPRequestHandler
import logging, json, pickle
import pandas as pd
from urlparse import parse_qs


class  RequestHandler(BaseHTTPRequestHandler): 

         
    def read_POST_data(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")
        return post_data

    def _set_headers(self):       
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """ GET is reserved for "/stats" and "/loadModelAtURL?url=url10;model=model10.pkl"""
        self._set_headers()
        if self.path == "/stats":
            resp = {'started_at':str(self.server.started_at)}
            for url in self.server.models.keys():
                model,filename = self.server.models[url]
                resp[url] = (self.server.stats[url],filename)
            response = json.dumps(resp)
            self.wfile.write(response.encode("utf-8"))
        elif "/loadModelAtURL" in self.path:
            query = self.path.replace("/loadModelAtURL?","")
            params = parse_qs(query)
            print params
            url = params["url"][0]
            model_file = params["model"][0]
            f = open(model_file,"r")
            model = pickle.load(f)
            f.close()
            self.server.models[url] = (model,model_file)
        else:
            # 404
            pass


    def do_POST(self):
        """ POST is reserved for doing only model predictions at urls defined in webscikit.conf"""
        self._set_headers()
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
                self.wfile.write(response.encode("utf-8"))
            if not model_found:
                pass
