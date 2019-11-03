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

BRAIN_ML_KEY=os.environ.get('API_KEY', "gvfv36vRto//lE2C68O8kOenlCU62cNj2V3G9mhvSn+dUE+VWWVCt0vBzvqLl/kQC69VAHMfwpuSkFkwaIFnxQ==")
BRAIN_URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/ead721b8b1f44935986b706588a2e35b/services/cc338680cb684d819f2bd7c1df482abd/execute?api-version=2.0&details=true")
# Deployment environment variables defined on Azure (pull in with os.environ)

# Construct the HTTP request header
# HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ API_KEY)}

HEADERS = {'Content-Type':'application/json', 'Authorization':('Bearer '+ BRAIN_ML_KEY)}

# Our main app page/route
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
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
                    # "Values": [
                    #     [
                    #     15000.000,
                    #     "",
                    #     "Employed",
                    #     62902,
                    #     69,
                    #     14,
                    #     94,
                    #     159.383042
                    #     ]
                    "Values": [
                        [
                        form.lifetime.data.lower(),
                        "",
                        form.employment.data.lower(),
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
        #req = urllib.request.Request(URL, body, HEADERS)
        req = urllib.request.Request(BRAIN_URL, body, HEADERS)

        # Send this request to the AML service and render the results on page
        try:
            # response = requests.post(URL, headers=HEADERS, data=body)
            response = urllib.request.urlopen(req)
            #print(response)
            #print(response[0].Results.output1)
            respdata = response.read()
            result = json.loads(str(respdata, 'utf-8'))
            result = do_something_pretty(result)
            #result = json.dumps(result, indent=4, sort_keys=True)
            #result=result1["Results"]["output1"]["value"]["Values"][7]
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
            #print(err)

    # Just serve up the input form
    return render_template(
        'form.html',
        form=form,
        title='Run App',
        year=datetime.now().year,
        message='Demonstrating a website using Azure ML Api')


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

def do_something_pretty(jsondata):
    """We want to process the AML json result to be more human readable and understandable"""
    import itertools # for flattening a list of tuples below

    # We only want the first array from the array of arrays under "Value" 
    # - it's cluster assignment and distances from all centroid centers from k-means model
    value = jsondata["Results"]["output1"]["value"]["Values"][0]
    #valuelen = len(value)
    print(value)
    # Convert values (a list) to a list of tuples [(cluster#,distance),...]
    # valuetuple = list(zip(range(valuelen-1), value[1:(valuelen)]))
    # Convert the list of tuples to one long list (flatten it)
    # valuelist = list(itertools.chain(*valuetuple))

    # Convert to a tuple for the list
    # data = tuple(list(value[0]) + valuelist)
    
    # Build a placeholder for the cluster#,distance values
    #repstr = '<tr><td>%d</td><td>%s</td></tr>' * (valuelen-1)
    # print(repstr)
    output='The response from Customer : ' +value[8]
    # Build the entire html table for the results data representation
    #tablestr = 'Cluster assignment: %s<br><br><table border="1"><tr><th>Cluster</th><th>Distance From Center</th></tr>'+ repstr + "</table>"
    #return tablestr % data
    return output
    