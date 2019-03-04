
from blackduck.HubRestApi import HubInstance
import requests
import json
from sys import argv

hub = HubInstance()
cleanup = len(argv) > 1
total_removed = 0

    
def get_components(limit=1000, offset=0, parameters={}):
    parameters['limit'] = str(limit)
    parameters['offset'] = str(offset)
    url = hub.config['baseurl'] + "/api/components" + hub._get_parameter_string(parameters)
    headers = hub.get_headers()
    response = requests.get(url, headers=headers, verify = not hub.config['insecure'])
    jsondata = response.json()
    print(response.status_code)
    return jsondata

#
# main
# 

# components = get_components(limit=5, parameters={'q':"versionName:borgy"})
components = get_components(limit=5, parameters={'q':".versionName:requests"})
print(components)
if 'totalCount' in components and components['totalCount'] > 0:
    for component in components['items']:
        print(component)

print("Total remove: {}".format(total_removed))





        