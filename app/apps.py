import yaml
import json
from lib.composegenerator import convertToDockerComposeYML
from lib.validate import findAndValidateApps
from lib.metadata import getAppRegistry
import os

# Loads an app.yml and calls removeMetadata on it, then returns the output of that
def getApp(app):
    with open(app, 'r') as f:
        app = yaml.safe_load(f)
    return convertToDockerComposeYML(app)

apps = findAndValidateApps("../apps")
# Loop through the apps and generate valid compose files from them, then put these into the app dir
for app in apps:
    composeFile = os.path.join("..", "apps", app, "docker-compose.yml")
    appYml = os.path.join("..", "apps", app, "app.yml")
    with open(composeFile, "w") as f:
        f.write(yaml.dump(getApp(appYml)))

print("Generated configuration successfully")

registry = getAppRegistry("../apps")
# Write the registry to ../apps/registry.json
with open(os.path.join('..', 'apps', 'registry.json'), 'w') as f:
    f.write(json.dumps(registry, sort_keys=True, indent=4))
