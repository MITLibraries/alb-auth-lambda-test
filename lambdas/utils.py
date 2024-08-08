# type: ignore
# ruff: noqa

import jwt
import requests
import base64
import json

REGION = "us-east-1"


def parse_oidc_data(encoded_jwt, verify=True, options=None):
    # parse JWT headers
    jwt_headers_str = encoded_jwt.split(".")[0]
    decoded_jwt_headers_json = base64.b64decode(jwt_headers_str).decode()
    jwt_headers = json.loads(decoded_jwt_headers_json)

    # get the key id from headers
    kid = jwt_headers["kid"]

    # get the public key from regional endpoint
    url = "https://public-keys.auth.elb." + REGION + ".amazonaws.com/" + kid
    pub_key = requests.get(url).text

    # decode payload
    return jwt.decode(
        encoded_jwt,
        pub_key,
        algorithms=["ES256"],
        verify=verify,
        options=options,
    )


def simulate(event):
    response = requests.post(
        "http://localhost:9000/2015-03-31/functions/function/invocations",
        json=event,
    )
    try:
        return json.loads(response.json()["body"])
    except:
        return response.content
