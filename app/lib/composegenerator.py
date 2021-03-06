import re

# Fun fact: All functions below have been generated by GitHub Copilot
# Thanks a lot, Copilot!

# Helper functions

# Return a list of env vars in a string, supports both $NAM§ and ${NAME} format for the env var
# This can potentially be used to get around permissions, so this check is critical for security
# Please report any security vulnerabilities you find in this check to aaron.dewes@web.de
def getEnvVars(string):
    envVars = re.findall(r'\$\{.*?\}', string)
    newEnvVars = re.findall(r"\$(?!{)([\S]+)", string)
    return [envVar[2:-1] for envVar in envVars] + newEnvVars


# Check if an array only contains values which are also in another array
def checkArrayContainsAllElements(array: list, otherArray: list):
    for element in array:
        if element not in otherArray:
            return False
    return True

# Combines two objects
# If the key exists in both objects, the value of the second object is used
# If the key does not exist in the first object, the value from the second object is used
# If a key contains a list, the second object's list is appended to the first object's list
# If a key contains another object, these objects are combined
def combineObjects(obj1, obj2):
    for key in obj2:
        if key in obj1:
            if isinstance(obj1[key], list):
                obj1[key] = obj1[key] + obj2[key]
            elif isinstance(obj1[key], dict):
                obj1[key] = combineObjects(obj1[key], obj2[key])
            else:
                obj1[key] = obj2[key]
        else:
            obj1[key] = obj2[key]
    return obj1

# Main functions

permissions = {
    "lnd": {
        "env": {
            "LND_IP": "${LND_IP}",
            "LND_GRPC_PORT": "${LND_GRPC_PORT}",
            "LND_REST_PORT": "${LND_REST_PORT}",
            "BITCOIN_NETWORK": "${BITCOIN_NETWORK}"
        },
        "volumes": [
            '${LND_DATA_DIR}:/lnd:ro'
        ]
    },
    "bitcoind": {
        "env": {
            "BITCOIN_IP":       "${BITCOIN_IP}",
            "BITCOIN_NETWORK":  "${BITCOIN_NETWORK}",
            "BITCOIN_P2P_PORT": "${BITCOIN_P2P_PORT}",
            "BITCOIN_RPC_PORT": "${BITCOIN_RPC_PORT}",
            "BITCOIN_RPC_USER": "${BITCOIN_RPC_USER}",
            "BITCOIN_RPC_PASS": "${BITCOIN_RPC_PASS}",
            "BITCOIN_RPC_AUTH": "${BITCOIN_RPC_AUTH}"
        }
    }
}

def convertContainerPermissions(app):
    for container in app['containers']:
        # Prepare for the next step
        if(container['env']):
            container['customEnv'] = container['env']
            del container['env']
        if container['permissions']:
            for permission in container['permissions']:
                if(permissions[permission]):
                    container = combineObjects(container, permissions[permission])
            del container['permissions']
    return app

def convertContainersToServices(app: dict):
    app['services'] = {}
    for container in app['containers']:
        app['services'][container['name']] = container
        del app['services'][container['name']]['name']
    del app['containers']
    return app

def validateEnv(app: dict):
    # For every container of the app, check if all env vars in the strings in customEnv are defined in env
    for container in app['containers']:
        if(container['customEnv']):
            for envVar in container['customEnv']:
                # Get first value of the envVar dict
                envVarValue = envVar[list(envVar.keys())[0]]
                envVarsInSring = getEnvVars(envVarValue)
                for envVarInString in envVarsInSring:
                    if envVarInString not in container['env'].keys():
                        print("Error: Environment variable " + envVarInString + " is not allowed")
                        exit(1)
                container['env'][list(envVar.keys())[0]] = envVarValue
        del container['customEnv']

    return app

# Converts the data of every container in app['containers'] to a volume, which is then added to the app
def convertDataDirToVolume(app: dict):
    for container in app['containers']:
            container['volumes'].append('${APP_DATA_DIR}/' + container['name'] + '/:' + container['data'])
            del container['data']
    return app

def convertToDockerComposeYML(app: dict):
    # The compose file doesn't care about metadata
    if(app['metadata']):
        del app['metadata']
    app = convertContainerPermissions(app)
    app = validateEnv(app)
    app = convertDataDirToVolume(app)
    app = convertContainersToServices(app)
    # Set version to 3.7 (current compose file version)
    app = { 'version': '3.7', **app }
    return app