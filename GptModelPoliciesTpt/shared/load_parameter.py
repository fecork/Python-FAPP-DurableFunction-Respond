from typing import Dict
from kedro.config import ConfigLoader, MissingConfigException

def load_parameters() -> Dict:
    """
    Funtion for load parameters from /parameters.
    """

    conf_loader = ConfigLoader(conf_source="conf", env="local")

    try:
        parameters = conf_loader.get("parameters*", "parameters*/**")
    except MissingConfigException:
        parameters = {}

    return parameters


def load_credentials() -> Dict:
    """
    This is a function for  search the credentials.
    in credential.yml.
    """

    conf_loader = ConfigLoader(conf_source="conf", env="local")

    try:
        credentials = conf_loader.get("credentials*", "credentials*/**")
    except MissingConfigException:
        credentials = {}

    return credentials
