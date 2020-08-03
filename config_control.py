import os
import sys
import json

def initialize_server(ignore_exception = True):
    try:
        with open("configuration.json", encoding='UTF8') as f:
            server_configuration = json.load(f)

        sys.path.append(os.path.abspath(server_configuration['dpm_module_location']))
        return server_configuration
    except FileNotFoundError as e:
        if not ignore_exception:
            raise e
        else:
            return {}
    except Exception as e:
        raise e