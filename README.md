# alb-auth-lambda-test

## Development

- To preview a list of available Makefile commands: `make help`
- To install with dev dependencies: `make install`
- To update dependencies: `make update`
- To run unit tests: `make test`
- To lint the repo: `make lint`

## Running Locally with Docker

<https://docs.aws.amazon.com/lambda/latest/dg/images-test.html>

- Build the container:

  ```bash
  docker build -t alb-auth-lambda-test:latest .
  ```

- Run the default handler for the container:

  ```bash
  docker run -e WORKSPACE=dev -p 9000:8080 alb-auth-lambda-test:latest
  ```

- Use a utility function to simulate a stripped down event passed to the lambda that contains authentication headers we are expecting:

  ```shell
  pipenv run ipython
  ```
  
  ```python
  from lambdas.utils import *
  
  # This event object contains some headers set by ALB authentication with Touchstone.
  # The header 'x-amzn-oidc-data' which we are parsing is expired, so we include a 
  #   'jwt_parse_options' key in the dictionary that tells our parser to ignore expired 
  #   token.  Normally, this key won't be present in the event , and the parsing will not 
  #   bypass this check.
  event = {
    "httpMethod": "GET",
    "path": "/",
    "queryStringParameters": {},
    "headers": {
      "x-amzn-oidc-accesstoken": "eyJraWQiOiJHX0QxcWpaWHdaWm51Q0w1djE2dzBJdC1vbnpHUy1oZkJDN0NTVld4dFFzIiwidHlwIjoiYXBwbGljYXRpb25cL29rdGEtaW50ZXJuYWwtYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULjlQYTBsNERhSzBRUHJwaEVvVy1zbVJkeEFiZnhzTDZpV3JIZ1ZPeU9SWWciLCJpc3MiOiJodHRwczovL29rdGEubWl0LmVkdSIsImF1ZCI6Imh0dHBzOi8vb2t0YS5taXQuZWR1Iiwic3ViIjoiY2FidXRsZXJAbWl0LmVkdSIsImlhdCI6MTcyMzA2NDAxOSwiZXhwIjoxNzIzMDY3NjE5LCJjaWQiOiIwb2Foa2lsZzV1ajRZUmZjWTY5NyIsInVpZCI6IjAwdTJwNXVyMWxES1VuaWEyNjk3Iiwic2NwIjpbIm9wZW5pZCJdLCJhdXRoX3RpbWUiOjE3MjMwNjQwMTZ9.ojb8-fH7fhuh326bfJFIEASDBCJSK0lhPH2KsqN1jr9P0dS5NQl7SmiDl2kevYF6QTBE67sDK-xBTyP48Ip-Dmr0Y9s9kNBHjvV_1Wcuhx6nKYlPv4W2wQ-cW725QSGQFni-hDTsvBXiYMDOHrgedzMftw21W9O4DhG-cGqy4OMxMHuQ2sMgCdmpUiNtI77GiiiKELuHvzWaAlRMcx_qGVJ8KyA6xid81NSodH-eltIKxg2ElxzGCbCSK-6VPYqgDT3-YRxzQ_V7L5bB_FNLiuGjPP9NcRHDQzu_-gAehN-wlSsT_GXP9R3QrSqJ8rw7JThmtYKlNO_eH8An7Oon6A",
      "x-amzn-oidc-data": "eyJ0eXAiOiJKV1QiLCJraWQiOiIzZWNiNjU3My1kYTU2LTQ5NDYtOGEwMi1hOTRhNjEzNzMyYmQiLCJhbGciOiJFUzI1NiIsImlzcyI6Imh0dHBzOi8vb2t0YS5taXQuZWR1IiwiY2xpZW50IjoiMG9haGtpbGc1dWo0WVJmY1k2OTciLCJzaWduZXIiOiJhcm46YXdzOmVsYXN0aWNsb2FkYmFsYW5jaW5nOnVzLWVhc3QtMToyMjIwNTM5ODAyMjM6bG9hZGJhbGFuY2VyL2FwcC9zdGFuZGFyZC1ub24tcHVibGljLzIyYzg2ZWFkODgzMWJhOTYiLCJleHAiOjE3MjMwNjQxMzl9.eyJzdWIiOiIwMHUycDV1cjFsREtVbmlhMjY5NyIsImV4cCI6MTcyMzA2NDEzOSwiaXNzIjoiaHR0cHM6Ly9va3RhLm1pdC5lZHUifQ==.8zBgqNH9SD-7Wp_Z9r8lCzLLhmOxTcgdALdbt20T-4MDUSDPuv2a-6QrleXkqCfsen9bmUJPQtkdW6YXHsSI4g==",
      "x-amzn-oidc-identity": "00u2p5ur1lDKUnia2697",
    },
    "isBase64Encoded": False,
    "jwt_parse_options": {
      "verify_exp": False
    }
  }
  
  simulate(event)
  ```

## Environment Variables

### Required

```shell
None currently required...
```

### Optional

_Delete this section if it isn't applicable to the PR._

```shell
<OPTIONAL_ENV>=### Description for optional environment variable
```