import logging
import spacy
import json
import os
import sys

import pandas as pd
from typing import Dict
from kedro.config import ConfigLoader, MissingConfigException


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

# from validators_respond import validate_boolean, validate_charge_number, validate_structure_json, validate_refund
# from shared.load_parameter import load_parameters




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

nlp = spacy.load("en_core_web_sm")
loaded_parameters = load_parameters()
list_questions = loaded_parameters["list_question_fare_rules"].split(",")
print(list_questions)