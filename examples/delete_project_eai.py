'''
Created on March 4, 2019

@author: gsnyder

Delete a project and its scans

import argparse
import csv
import logging
import sys

from blackduck.HubRestApi import HubInstance

parser = argparse.ArgumentParser("A program that will delete a project along with its scans")
parser.add_argument("project", help="Project name")
parser.add_argument("-k", "--keep_scans", action = 'store_true', default=False, help="Use this option if you want to keep scans associated with the project-versions. Default is False, scans will be deleted.")
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

hub = HubInstance()

hub.delete_project_by_name(args.project, save_scans=args.keep_scans)

'''
from blackduck.HubRestApi import HubInstance
from pprint import pprint

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("project_name")
parser.add_argument("run_delete")

args = parser.parse_args()

hub = HubInstance()

projects = hub.get_projects(parameters={'q':"name:{}".format(args.project_name)})

from pprint import pprint

if 'totalCount' in projects and projects['totalCount'] > 0:
	for project in projects['items']:
		if project['name'] != args.project_name:
			continue
		# pprint(project)

		project_versions = hub.get_project_versions(
			project
		)

		project_version_codelocations = None
		if 'totalCount' in project_versions and project_versions['totalCount'] > 0:
			for project_version in project_versions['items']:
				# pprint(project_version)
				project_version_codelocations = hub.get_version_codelocations(project_version)

				if 'totalCount' in project_version_codelocations and project_version_codelocations['totalCount'] > 0:
					code_location_urls = [c['_meta']['href'] for c in project_version_codelocations['items']]
					for code_location_url in code_location_urls:
						print("Deleting code location at: {}".format(code_location_url))
						if args.run_delete == "1":
							a = hub.execute_delete(code_location_url)
							print(a)
				else:
					print("Did not find any codelocations (scans) in version {} of project {}".format(project_version['versionName'], args.project_name))

				print("Deleting project-version {} at: {}".format(project_version['versionName'], project_version['_meta']['href']))
				if args.run_delete == "1":
					a = hub.execute_delete(project_version['_meta']['href'])
					print(a)
		else:
			print("Did not find versions in project {}".format(args.project_name))
		
	print("Deleting project {} at: {}".format(project['name'], project['_meta']['href']))
	if args.run_delete == "1":
		a = hub.execute_delete(project['_meta']['href'])
		print(a)
else:
	print("Did not find project with name {}".format(args.project_name))