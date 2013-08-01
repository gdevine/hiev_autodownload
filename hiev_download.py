'''
Python script to perform a HIEv API filter search and then download of files based on the returned urls

Author: Gerard Devine
Date: July 2013
'''

import json
import urllib2
import yaml


# --Read in parameters set from config file
stram = open("config.yaml", "r")
paramset = yaml.load_all(stram)


# --Iterate over each individual entry in the parameters set
for entry in paramset:
    request_url = entry['request_url']
    api_token = entry['api_token']
    variables = entry['variables']

    # --Set up my request
    request_headers = {'Content-Type' : 'application/json; charset=UTF-8','X-Accept': 'application/json'}
    request_data    = json.dumps({"auth_token": api_token, "variables" : variables})
    
    
    # --Handle the returned response from the HIEv server
    request  = urllib2.Request(request_url, request_data, request_headers)
    response = urllib2.urlopen(request)
    js = json.load(response)
    
    
    # --For each element returned pass the url to the download API and download
    for item in js:
        download_url = item["url"]+'?'+'auth_token=%s' %api_token
        request  = urllib2.Request(download_url)
        f = urllib2.urlopen(request)
    
        # Open a local file for writing 
        with open(item["filename"], "wb") as local_file:
            local_file.write(f.read())
            
    #TODO Print a summary of activity to a local log file
    #TODO Abstract filter variables out to a configuration file
    print 'Total files = %s' %len(js)
