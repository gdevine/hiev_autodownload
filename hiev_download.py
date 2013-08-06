'''
Python script to perform a HIEv API filter search and then download of files 
based on the returned urls. This script is informed by a settings.yaml file.

Author: Gerard Devine
Date: July 2013
'''

import os
import json
import urllib2
import yaml
from datetime import date, datetime, timedelta


# --Read the yaml settings file into python  
try:
    stram = open("local_settings.yaml", "r") #for running in a dev environment
except:
    stram = open("settings.yaml", "r")
settings = yaml.load(stram)

# --Parse global values
request_url = settings['request_url']
api_token = settings['api_token']

# --Open log file for writing and append date/time stamp into file for a new entry
logfile = 'log_'+str(date.today())+'.txt'
log = open(os.path.join(os.getcwd(), 'logs', logfile), 'a')
log.write('\n----------------------------------------------- \n')
log.write('------------  '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'  ------------ \n')
log.write('----------------------------------------------- \n')

# --Iterate over each individual entry in the params set
for entry in settings['params']:
    variables = entry['variables']
    ingest = entry['ingest']
    
    # --Begin a log entry for this iteration
    log.write(' -For files being downloaded to %s \n' %entry['dirname'])

    # --Set up the http request (depending on ingest period, daily etc)
    request_headers = {'Content-Type' : 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
    if ingest == 'daily': #only grab matching data uploaded from the last day
        upload_from_date = str(date.today() - timedelta(days=1))  
        request_data = json.dumps({'auth_token': api_token, 'upload_from_date': upload_from_date, 'variables' : variables})
    else: #grab all matching data
        request_data = json.dumps({'auth_token': api_token, 'variables' : variables})
        
    # --Handle the returned response from the HIEv server
    request  = urllib2.Request(request_url, request_data, request_headers)
    response = urllib2.urlopen(request)
    js = json.load(response)
    
    # --If there are files to be downloaded, then set up a directory to hold them (if not existing)
    if len(js):
        dest_dir = os.path.join(os.getcwd(), 'data', entry['dirname'])
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir) 
        # --For each element returned pass the url to the download API and download
        for item in js:
            download_url = item['url']+'?'+'auth_token=%s' %api_token
            request  = urllib2.Request(download_url)
            f = urllib2.urlopen(request)
                    
            # --Write the file
            with open(os.path.join(dest_dir, item['filename']), 'w') as local_file:
                local_file.write(f.read())
            local_file.close()
         
        log.write('  Total files downloaded = %s \n' %len(js))
    else:
        log.write('  No files matched the search params \n')
        

# --Close log file
log.close()
