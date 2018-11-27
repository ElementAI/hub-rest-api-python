'''
Created on Nov 13, 2018

@author: gsnyder

Given a project name, a version name, delete the project-version and any scans associated with it

'''
from blackduck.HubRestApi import HubInstance
from pprint import pprint

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("project_name")

args = parser.parse_args()

hub = HubInstance()

projects = hub.get_projects(parameters={'q':"name:{}".format(args.project_name)})

total_version = 0
total_code_location = 0
if 'totalCount' in projects and projects['totalCount'] > 0:
	for project in projects['items']:
		print(project['name'])
		project_versions = hub.get_project_versions(
			project
		)

		if 'totalCount' in project_versions and project_versions['totalCount'] > 0:
			for version in project_versions['items']:
				if version['phase'] != 'DEVELOPMENT':
					continue
				total_version += 1
				print("\t- {}".format(version['versionName']))

				project_version_codelocations = hub.get_version_codelocations(version)
				print("\t\t- {} codes location".format(project_version_codelocations['totalCount']))
				total_code_location += project_version_codelocations['totalCount']

				if 'totalCount' in project_version_codelocations and project_version_codelocations['totalCount'] > 0:
					code_location_urls = [c['_meta']['href'] for c in project_version_codelocations['items']]
					for code_location_url in code_location_urls:
						print("Deleting code location at: {}".format(code_location_url))
						hub.execute_delete(code_location_url)
				else:
					print("Did not find any codelocations (scans) in version {} of project {}".format(version['versionName'], args.project_name))
				print("Deleting project-version at: {}".format(version['_meta']['href']))
				hub.execute_delete(version['_meta']['href'])

print("Total version: {}".format(total_version))
print("Total code location: {}".format(total_code_location))
