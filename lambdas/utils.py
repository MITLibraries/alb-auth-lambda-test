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


def prepare_logout_response():
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "statusDescription": "200 OK",
        "headers": {
            "Set-cookie": "AWSALBAuthNonce=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 "
            "GMT\nAWSELBAuthSessionCookie-oidc-poc-0=; Path=/; "
            "Expires=Thu, 01 Jan 1970 00:00:00 GMT",
            "Content-Type": "application/json",
        },
        "body": json.dumps(
            {
                "msg": "logout successful",
                "details": "Cookies `AWSALBAuthNonce` and "
                "`AWSELBAuthSessionCookie-oidc-poc-0` have been manually "
                "expired, meaning you are logged out of THIS "
                "application.  But your session remains active with "
                "Touchstone Okta.  Therefore a refresh of the restricted "
                "page will work, after a slight delay, as the ALB "
                "re-sets the logged in cookies for this domain.",
            }
        ),
    }
