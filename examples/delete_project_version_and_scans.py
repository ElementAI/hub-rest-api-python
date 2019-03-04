'''
Created on Nov 13, 2018

@author: gsnyder

Given a project name, a version name, delete the project-version and any scans associated with it


hub.delete_project_version_by_name(args.project_name, args.version_name, save_scans=args.save_scans)

'''
from blackduck.HubRestApi import HubInstance
import logging
import sys

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("project_name")
parser.add_argument("version_name")
parser.add_argument("-s", "--save_scans", action='store_true', help="Set this option to preserve the scans mapped to this project version")

args = parser.parse_args()

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', stream=sys.stderr, level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

hub = HubInstance()

projects = hub.get_projects(parameters={'q':"name:{}".format(args.project_name)})

if 'totalCount' in projects and projects['totalCount'] > 0:
	for project in projects['items']:
		if project['name'] != args.project_name:
			continue

		project_versions = hub.get_project_versions(
			project, 
			parameters={'q':"versionName:{}".format(args.version_name)}
		)

		project_version_codelocations = None
		if 'totalCount' in project_versions and project_versions['totalCount'] > 0:
			for project_version in project_versions['items']:
				if project_version['versionName'] != args.version_name:
					continue
				project_version_codelocations = hub.get_version_codelocations(project_version)

				if 'totalCount' in project_version_codelocations and project_version_codelocations['totalCount'] > 0:
					code_location_urls = [c['_meta']['href'] for c in project_version_codelocations['items']]
					for code_location_url in code_location_urls:
						print("Deleting code location at: {}".format(code_location_url))
						hub.execute_delete(code_location_url)
				else:
					print("Did not find any codelocations (scans) in version {} of project {}".format(args.version_name, args.project_name))

				print("Deleting project-version {} at: {}".format(project_version['versionName'], project_version['_meta']['href']))
				hub.execute_delete(project_version['_meta']['href'])
		else:
			print("Did not find version with name {} in project {}".format(args.version_name, args.project_name))
else:
	print("Did not find project with name {}".format(args.project_name))
