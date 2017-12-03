# webscikit
Webscikit is a set of tools to run a HTTPServer as a JSON Webservice for scikit-learn predictions. It comes with two examples: boston and boston2

It is work in progress, so it comes with no guarantee.

The server can handle multiple models. The models and urls are registered at webscikit.conf .


If you wan to run the examples:

source export_WEBSCIKITMODELSPATH.sh

cd server/

./webserver.py
 
cd ../example/requests/

./curl_boston.sh

./curl_boston2.sh


