#!/usr/bin/env python3

import yaml
import json
from lib.composegenerator import convertToDockerComposeYML
from lib.validate import findAndValidateApps
from lib.metadata import getAppRegistry
import os
import argparse
import requests
from sys import argv

# Initializes an argument parser with the descrition "Manage apps on your Citadel"
parser = argparse.ArgumentParser(description="Manage apps on your Citadel")
# Syntax: app.py [action] [app]
# action: What to do with the app (database) either install, remove, list, download, update, compose, start, stop, restart or logs
# app: The app to be used (optional, only for install, remove, compose, start, stop, restart, logs)
# If no action is specified, the list action is used
# If no app is specified, but the action is install, remove, compose, start, stop, restart or logs, print an error message and exit

# Parses the arguments
parser.add_argument('action', help='What to do with the app (database) either install, remove, list, download, update, update-online, compose, start, stop, restart or logs')
parser.add_argument('app', help='The app to be used (optional, only for install, remove, compose, start, stop, restart, logs)', nargs='?', default=None)
args = parser.parse_args()

# Returns a list of every argument after the second one in sys.argv joined into a string by spaces
def getArguments():
    arguments = ""
    for i in range(3, len(argv)):
        arguments += argv[i] + " "
    return arguments

# If no action is specified, the list action is used
if args.action is None:
    args.action = 'list'

# If the action is install, remove, compose, start, stop, restart or logs, the app is required
if args.action in ['install', 'remove', 'compose', 'start', 'stop', 'restart', 'logs'] and args.app is None:
    print('Error: No app specified')
    exit(1)

def getAppYml(name):
    url = 'https://raw.githubusercontent.com/runcitadel/compose/main/apps/' + name + '/' + 'app.yml'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return False

def getAppYmlPath(app):
    return os.path.join("..", "apps", app, 'app.yml')

def update():
    apps = findAndValidateApps("../apps")
    # Loop through the apps and generate valid compose files from them, then put these into the app dir
    for app in apps:
        composeFile = os.path.join("..", "apps", app, "docker-compose.yml")
        appYml = os.path.join("..", "apps", app, "app.yml")
        with open(composeFile, "w") as f:
            f.write(yaml.dump(getApp(appYml), sort_keys=False))
    print("Generated configuration successfully")

    registry = getAppRegistry(apps, "../apps")
    # Write the registry to ../apps/registry.json
    with open(os.path.join('..', 'apps', 'registry.json'), 'w') as f:
        f.write(json.dumps(registry, sort_keys=True, indent=4))
    print("Wrote registry to registry.json")

def download():
    if(args.app is None):
        apps = findAndValidateApps("../apps")
        for app in apps:
            data = getAppYml(app)
            if data:
                with open(getAppYmlPath(app), 'w') as f:
                    f.write(data)
            else:
                print("Warning: Could not download " + app)
    else:
        data = getAppYml(args.app)
        if data:
            with open(getAppYmlPath(args.app), 'w') as f:
                f.write(data)
        else:
            print("Warning: Could not download " + args.app)

# Loads an app.yml and converts it to a docker-compose.yml
def getApp(app):
    with open(app, 'r') as f:
        app = yaml.safe_load(f)
    return convertToDockerComposeYML(app)

def compose(app, arguments):
    # Runs a compose command in the app dir
    # Before that, check if a docker-compose.yml exists in the app dir
    composeFile = os.path.join("..", "apps", app, "docker-compose.yml")
    if not os.path.isfile(composeFile):
        print("Error: Could not find docker-compose.yml in " + app)
        exit(1)
    # Save the previous working directory and return to it later
    oldDir = os.getcwd()
    os.chdir(os.path.join("..", "apps", app))
    os.system("docker-compose --env-file ../../.env" + arguments)
    os.chdir(oldDir)

if args.action == 'install':
    print("Not implemented yet")
    exit(1)
elif args.action == 'remove':
    print("Not implemented yet")
    exit(1)
elif args.action == 'compose':
    compose(args.app, getArguments())
    exit(0)
elif args.action == 'start':
    compose(args.app, 'up')
    exit(0)
elif args.action == 'stop':
    compose(args.app, 'down')
    exit(0)
elif args.action == 'restart':
    compose(args.app, 'down')
    compose(args.app, 'up')
    exit(0)
elif args.action == 'logs':
    compose(args.app, 'logs ' + getArguments())
    exit(0)
elif args.action == 'list':
    apps = findAndValidateApps("../apps")
    for app in apps:
        print(app)
    exit(0)
elif args.action == 'download':
    download()
    exit(0)     
elif args.action == 'update':
    update()
    exit(0)
elif args.action == 'update-online':
    download()
    update()
    exit(0)
else:
    print("Error: Unknown action")
    exit(1)
