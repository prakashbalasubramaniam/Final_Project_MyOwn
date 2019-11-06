"""
Routes and views for the flask application.
"""
import json
import urllib.request
import os

from datetime import datetime
from flask import render_template, request, redirect, app
from FlaskAppAML import app

from FlaskAppAML.forms import SubmissionForm

from .forms import Employment_choices

ML_KEY=os.environ.get('API_KEY', "gvfv36vRto//lE2C68O8kOenlCU62cNj2V3G9mhvSn+dUE+VWWVCt0vBzvqLl/kQC69VAHMfwpuSkFkwaIFnxQ==")
ML_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/ead721b8b1f44935986b706588a2e35b/services/cc338680cb684d819f2bd7c1df482abd/execute?api-version=2.0&details=true")
# Deployment environment variables defined on Azure (pull in with os.environ)

# Construct the HTTP request header

HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ ML_KEY)}

# Our main app page
@app.route('/')
def home():
    """Renders the contact page."""
    return render_template(
        'home.html',
        title='Gekkos Insurance',
        year=datetime.now().year,
        # message='Your contact page.'
    )

# Predictive response route
@app.route('/predictresponse', methods=['GET', 'POST'])
# @app.route('/home', methods=['GET', 'POST'])
# def home():
def predictresponse():
    """Renders the home page which is the CNS of the web app currently, nothing pretty."""

    form = SubmissionForm(request.form)

    # Form has been submitted
    if request.method == 'POST' and form.validate():

        # Plug in the data into a dictionary object 
        #  - data from the input form
        #  - text data must be converted to lowercase
        data = {
                "Inputs": {
                    "input1": {
                    "ColumnNames": [
                        "Customer Lifetime Value",
                        "Response",
                        "EmploymentStatus",
                        "Income",
                        "Monthly Premium Auto",
                        "Months Since Last Claim",
                        "Months Since Policy Inception",
                        "Total Claim Amount"
                    ],
                    "Values": [
                        [
                        form.lifetime.data.lower(),
                        "",
                        # form.employment.data.lower(),
                        dict(Employment_choices).get(form.employment.data),
                        form.income.data.lower(),
                        form.premium.data.lower(),
                        form.lastclaim.data.lower(),
                        form.inception.data.lower(),
                        form.claimamount.data.lower()
                        ]
                    ]
                    }
                },
                "GlobalParameters": {}
                }

        # Serialize the input data into json string
        body = str.encode(json.dumps(data))

        # Formulate the request
        req = urllib.request.Request(ML_URL, body, HEADERS)

        # Send this request to the AML service and render the results on page
        try:

            response = urllib.request.urlopen(req)
            respdata = response.read()
            result = json.loads(str(respdata, 'utf-8'))
            result = do_something_pretty(result)

            return render_template(
                'result.html',
                title="Insurance Customer Marketing Response Prediction:",
                result=result)

        # An HTTP error
        except urllib.error.HTTPError as err:
            result="The request failed with status code: " + str(err.code)
            return render_template(
                'result.html',
                title='There was an error',
                result=result)
            

    # Just serve up the input form
    return render_template(
        'form.html',
        form=form,
        title='Run App',
        year=datetime.now().year,
        message='Demonstrating a website using Azure ML Api')


@app.route('/athena')
def athena():
    """Renders the contact page."""
    return render_template(
        'athena.html',
        title='AWS Athena & Tableau',
        year=datetime.now().year,
        # message='Your contact page.'
    )

@app.route('/custtrend')
def custtrend():
    """Renders the about page."""
    return render_template(
        'custtrend.html',
        title='Customer Base Trend Analysis',
        year=datetime.now().year,
        #message='Your application description page.'
    )

@app.route('/colab')
def colab():
    """Renders the contact page."""
    return render_template(
        'colab.html',
        title='Google CoLab',
        year=datetime.now().year,
        # message='Your contact page.'
    )

@app.route('/mlvalidation')
def mlvalidation():
    """Renders the mlvalidation page."""
    return render_template(
        'mlvalidation.html',
        title='Azure ML Validation through Python',
        year=datetime.now().year,
        # message='Your contact page.'
    )

@app.route('/premium')
def premium():
    """Renders the premium page."""
    return render_template(
        'premium.html',
        title='California Monthly Premium Estimate',
        year=datetime.now().year,
        # message='Your contact page.'
    )

def do_something_pretty(jsondata):
    """We want to process the AML json result to be more human readable and understandable"""
    import itertools # for flattening a list of tuples below

    # We only want the first array from the array of arrays under "Value" 
    # - it's cluster assignment and distances from all centroid centers from k-means model
    value = jsondata["Results"]["output1"]["value"]["Values"][0]
    
    print(value)

    output='The response from Customer : ' +value[8]

    return output
    