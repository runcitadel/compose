
import os
import yaml
from jsonschema import validate
import json

# Read in an app.yml file and pass it to the validation function
# Returns true if valid, false otherwise
def validateAppFile(file):
    with open(file, 'r') as f:
        app = yaml.safe_load(f)
    with open('./app-standard.json', 'r') as f:
        schema = json.loads(f.read())
    
    try:
        validate(app, schema)
        return True
    # Catch and log any errors, and return false
    except Exception as e:
        print(e)
        return False

# Lists all folders in a directory and checks if they are valid
# A folder is valid if it contains an app.yml file
# A folder is invalid if it doesn't contain an app.yml file
def findAndValidateApps(dir):
    apps = []
    for root, dirs, files in os.walk(dir):
        for name in dirs:
            app_dir = os.path.join(root, name)
            if os.path.isfile(os.path.join(app_dir, "app.yml")):
                apps.append(name)
    # Now validate all the apps using the validateAppFile function by passing the app.yml as an argument to it, if an app is invalid, remove it from the list
    for app in apps:
        if not validateAppFile(os.path.join(dir, app, "app.yml")):
            apps.remove(app)
    return apps
