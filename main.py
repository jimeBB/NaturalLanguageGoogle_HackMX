from flask import Flask, redirect, render_template, request

from google.cloud import automl_v1beta1 as automl
import argparse
import os
from automl_natural_language_predict import predict 

app = Flask(__name__)


@app.route('/')
def homepage():
    # Return a Jinja2 HTML template of the homepage.
    return render_template('homepage.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict(project_id, compute_region, model_id):
    project_id = "cdmx-safe-map"
    compute_region = "us-central1"
    model_id= "TCN3023487612629800943"
    automl_client = automl.AutoMlClient()

    # Create client for prediction service.
    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = automl_client.model_path(
        project_id, compute_region, model_id
    )

    

    text = request.form['comment']   
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT) 

    # Set the payload by giving the content and type of the file.
    payload = {"text_snippet": {"content": document, "mime_type": "text/plain"}}



    # params is additional domain-specific parameters.
    # currently there is no additional parameters supported.
    params = {}
    response = prediction_client.predict(model_full_id, payload, params)
    labels = response.payload
    #for result in response.payload:
        #if(result.classification.score >0.6):
                #print("{}".format(result.display_name))
                #print("Predicted class score: {}".format(result.classification.score))

    # [END automl_language_predict]

    return render_template('homepage.html', text=text, labels=labels)



#@app.route('/run_language', methods=['GET', 'POST'])
#def run_language():
    #automl_client = automl.AutoMlClient()

    # Create client for prediction service.
    #prediction_client = automl.PredictionServiceClient()

    # Retrieve inputted text from the form and create document object
    #text = request.form['text']
    #document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)

    # Retrieve response from Natural Language API's analyze_entities() method
    #response = client.analyze_entities(document)
    #entities = response.entities

    # Retrieve response from Natural Language API's analyze_sentiment() method
    #response = client.analyze_sentiment(document)
    #sentiment = response.document_sentiment

    # Return a Jinja2 HTML template of the homepage and pass the 'text'
    # and 'labels' variables to the frontend. These contain information retrieved
    # from the Auto ML Language API.
    #return render_template('homepage.html', text=text, labels=labels, )

@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
