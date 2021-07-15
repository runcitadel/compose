from email import generator
from jsonschema import validate
import yaml
import json
from lib.composegenerator import convertToDockerComposeYML

# Read in an app.yml file and pass it to the validation function
# Returns true if valid, false otherwise
def validateAppFile(file):
    with open(file, 'r') as f:
        app = yaml.safe_load(f)
    with open('app-standard.json', 'r') as f:
        schema = json.loads(f.read())
    
    try:
        validate(app, schema)
        return True
    # Catch and log any errors, and return false
    except Exception as e:
        print(e)
        return False

def validateApp(app):
    if validateAppFile(app):
        print("App manifest follows the app schema")
    else:
        print("App manifest doesn't follow the app schema")

# Loads an app.yml and calls removeMetadata on it, then returns the output of that
def getApp(app):
    with open(app, 'r') as f:
        app = yaml.safe_load(f)
    return convertToDockerComposeYML(app)


validateApp("app.yml")
outputCompose = yaml.dump(getApp("app.yml"), sort_keys=False)

# Write outputCompose to a file
with open('app-compose.yml', 'w') as f:
    f.write(outputCompose)

print("Generated configuration successfully")
