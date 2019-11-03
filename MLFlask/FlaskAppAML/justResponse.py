import urllib.request
import os
# If you are using Python 3+, import urllib instead of urllib2

import json 


data =  {

        "Inputs": {

                "input1":
                {
                  "ColumnNames": ["Customer Lifetime Value", "Response", "EmploymentStatus","Income", "Monthly Premium Auto", "Months Since Last Claim", "Months Since Policy Inception", "Total Claim Amount"],
                    "Values": [ [ "0", "value", "value", "0", "0", "0", "0","0"], [ "0", "value", "value", "0", "0", "0", "0","0" ], ]
                },        },
            "GlobalParameters": {
}
    }

body = str.encode(json.dumps(data))

url = os.environ.get('URL','https://ussouthcentral.services.azureml.net/workspaces/ead721b8b1f44935986b706588a2e35b/services/cc338680cb684d819f2bd7c1df482abd/execute?api-version=2.0&details=true')
api_key = os.environ.get('API_KEY','gvfv36vRto//lE2C68O8kOenlCU62cNj2V3G9mhvSn+dUE+VWWVCt0vBzvqLl/kQC69VAHMfwpuSkFkwaIFnxQ==') # Replace this with the API key for the web service)
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

# API_KEY = os.environ.get('API_KEY', "bqbOx/ih7sqf1YpFbTEBf9wyPA7WPcGGOomvMrTvwq4CC0KxgVPkU2grDnzYN/zqpx5xFUNWl1LOEK+C8L5zMw==")
# URL = os.environ.get('URL', "https://ussouthcentral.services.azureml.net/workspaces/db57e3c91aeb4c4c8c5b831eb3aa0bd5/services/375cb1234d0d4dc0b29774e6212acee5/execute?api-version=2.0&details=true")



req =urllib.request.Request(url, body, headers) 

try:
    response =urllib.request.urlopen(req)
    
    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
    # req = urllib.request.Request(url, body, headers) 
    # response = urllib.request.urlopen(req)

    result = response.read()
    print(result) 
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.msg)),
    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())

    print(json.loads(error.read()))  
