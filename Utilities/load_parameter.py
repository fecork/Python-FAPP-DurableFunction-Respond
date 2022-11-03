from typing import Dict
from kedro.config import ConfigLoader, MissingConfigException
from typing import Dict


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
