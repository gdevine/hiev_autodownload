'''
Python script to perform a HIEv API filter search and then download of files 
based on the returned urls. This script is informed by a config.yaml file.

Author: Gerard Devine
Date: July 2013
'''

import os
import json
import urllib2
import yaml


# --Read the yaml settings file into python 
stram = open("settings.yaml", "r")
settings = yaml.load(stram)

# --Parse global values
request_url = settings['request_url']
api_token = settings['api_token']

# --Iterate over each individual entry in the params set
for entry in settings['params']:
    variables = entry['variables']
    dest_dir = entry['dest_dir']

    # --Set up the http request
    request_headers = {'Content-Type' : 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
    request_data    = json.dumps({'auth_token': api_token, 'variables' : variables})
    
    # --Handle the returned response from the HIEv server
    request  = urllib2.Request(request_url, request_data, request_headers)
    response = urllib2.urlopen(request)
    js = json.load(response)
    
    # --For each element returned pass the url to the download API and download
    for item in js:
        download_url = item['url']+'?'+'auth_token=%s' %api_token
        request  = urllib2.Request(download_url)
        f = urllib2.urlopen(request)
    
        # --Create the directory to write to if not already existing 
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        # --Write the file
        with open(os.path.join(dest_dir, item['filename']), 'wb') as local_file:
            local_file.write(f.read())
            
    #TODO Print a summary of activity to a local log file
    #TODO Abstract filter variables out to a configuration file
    print 'Total files = %s' %len(js)
