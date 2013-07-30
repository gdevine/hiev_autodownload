'''
Python script to perform a HIEv API filter search and then download files based on the returned urls

Author: Gerard Devine
Date: July 2013
'''

import json
import urllib2


# --Set up my request
request_url     = "http://w0297.uws.edu.au/data_files/api_search"
request_headers = {'Content-Type' : 'application/json; charset=UTF-8','X-Accept': 'application/json'}
request_data    = json.dumps({"auth_token": "PSEsmywGqiEMyVni5r54", "variables" : ["AirTC"]})


# --Handle the returned response from the HIEv server
request  = urllib2.Request(request_url, request_data, request_headers)
response = urllib2.urlopen(request)
js = json.load(response)


# --For each element returned pass the url to the download API and download
for item in js:
    download_url = item["url"]+'?'+'auth_token=PSEsmywGqiEMyVni5r54'
    request  = urllib2.Request(download_url)
    f = urllib2.urlopen(request)

    # Open a local file for writing (temporarily assigning a name manually - need to pull actual filename from response)
    with open(item["filename"], "wb") as local_file:
        local_file.write(f.read())
        
    print 'Total files = %s' %len(js)