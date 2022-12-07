from urllib.request import urlopen
import os
import json

def get_jwk():
    url = os.environ["URLJWK"]
    response = urlopen(url)
    jwk = json.loads(response.read())
    return jwk
