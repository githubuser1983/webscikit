# webscikit
Webscikit is a set of tools to run a HTTPServer as a JSON Webservice for scikit-learn predictions. It comes with two examples: boston and boston2

It is work in progress, so it comes with no guarantee.

Features:

  * The server can handle multiple models. The models and urls are registered at webscikit.conf .

  * Multiple data-scientist could work locally on their own models, and then later deploy their model to the server.
  
  * The models can be deployed when the server is online.
  
  * Each model can save additional metadata needed to transform and predict new data.
  
  * You can easily start a new project with create_project.py newProjectName

If you wan to run the examples:

source export_WEBSCIKITMODELSPATH.sh

cd server/

./webserver.py
 
cd ../example/requests/

./curl_boston.sh

./curl_boston2.sh


