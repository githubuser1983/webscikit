import sys,csv,math
sys.path.insert(1,'/usr/local/lib/python2.7/dist-packages/')

from BaseHTTPServer import BaseHTTPRequestHandler
import logging, json
import pandas as pd

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
        if self.path == "/stats":
            print( """ Requests : 123
                   started_at : Datetime
                   Requests for url1 : 100
                   Requests for url2 :  20
                   Requests for url3 :   3 """)

        if self.path == "/loadModelAtURL":
            url = getRequestParam("url")
            model_file = getRequestParam("model")
            model = self.load_model(model_file)
            self.models[url] = model


    def do_POST(self):
        """ POST is reserved for doing only model predictions at urls defined in webscikit.conf"""
        self._set_headers()
        model_found = False
        for url in self.server.models.keys():
            if self.path == url:
                model_found = True
                model = self.server.models[url]
                data = self.read_POST_data()
                data = pd.read_json(data)
                prediction = model.transform_predict(data)
                json_prediction = prediction.to_json()
                response = json.dumps(json_prediction)
                self.wfile.write(response.encode("utf-8"))
            if not model_found:
                pass
