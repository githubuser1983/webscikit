# webscikit
Webscikit is a set of tools to run a HTTPServer as a JSON Webservice for scikit-learn predictions. It comes with two examples: iris and boston

It is work in progress, so it comes with no guarantee.

The server can handle multiple models. The models and urls are registered at webscikit.conf .


If you want to adapt it, see the following:

models.py
fit_boston.py
fit_iris.py
webscikit.conf


If you wan to run the examples:

python webserver.py

bash curl_boston.sh
bash curl_iris.sh
