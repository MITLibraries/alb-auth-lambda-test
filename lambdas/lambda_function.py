# type: ignore
# ruff: noqa

import json
import time

from lambdas.utils import parse_oidc_data

REGION = "us-east-1"


def lambda_handler(event, context):
    """
    https://docs.aws.amazon.com/elasticloadbalancing/latest/application/lambda-functions.html#prepare-lambda-function
    https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html#user-claims-encoding

    TODOs
        - consider parsing token as well?
        - are there parts of this we can cache?
    """
    print(json.dumps(event))

    error = None
    oidc_data = None

    # allow custom key for passing options to JWT decoding
    # supports parsing an expired signature, e.g. {'verify_exp': False}
    options = event.get("jwt_parse_options")

    t0 = time.time()
    try:
        oidc_data = parse_oidc_data(
            event["headers"]["x-amzn-oidc-data"],
            options=options,
        )
    except Exception as exc:
        error = exc
    parse_elapsed = time.time() - t0

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "statusDescription": "200 OK",
        "headers": {"Set-cookie": "cookies", "Content-Type": "application/json"},
        "body": json.dumps(
            {
                "lambda_event": event,
                "oidc_data": oidc_data,
                "oidc_access_token": "Currently not parsing...",
                "error": error,
                "parse_elapsed": parse_elapsed,
            }
        ),
    }
