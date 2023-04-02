import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'fsnd-mdw.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'udacity_coffeshop_api'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
This Method checks if there is an Authorization header included in the request and returns the token
'''
def get_token_auth_header():
    try:
        # check for Authorization header, extract it and check against emptyness
        if "Authorization" not in request.headers:
            raise AuthError(error={"code":"invalid header", "description": "header does not contain authorization token"}, status_code=401)
        headerTokenString = request.headers["Authorization"]
        if headerTokenString is None:
            raise AuthError(error={"code":"invalid header", "description": "no headertoken string included"}, status_code=401)
        # split non-empty Bearer token and check if it is divided into two parts -> return second part containing JWT
        headerTokenParts = headerTokenString.split(" ")
        if len(headerTokenParts) != 2:
            raise AuthError(error={"code":"invalid header", "description": "token header contains more than two parts"}, status_code=401)
        return headerTokenParts[1]
    # errorhandling
    except Exception as e:
        if isinstance(e, AuthError):
            raise AuthError(e.error, e.status_code)
        else:
            raise AuthError(error={"code":"invalid header", "description": "token header could not be read"}, status_code=401)

'''
This function checks if the permissions in the payload match to the permissions required for the endpoint.
'''
def check_permissions(permission, payload):
    try:
        # check if permissions are needed and part of the payload
        if permission == "":
            return True
        if "permissions" not in payload.keys():
            raise AuthError(error={"error": "no permissions"}, status_code=403)
        # check if permissions match in both parts
        if permission in payload["permissions"]:
            return True
        else:
            raise AuthError(error={"error": "not permitted"}, status_code=403)
    # errorhandling
    except Exception as e:
        if isinstance(e, AuthError):
            raise AuthError(e.error, e.status_code)
        else:
            raise AuthError(error={"code":"invalid header", "description": "permission could not be checked"}, status_code=401)
    

'''
@Done implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    try:
        tokenKid = jwt.get_unverified_header(token)["kid"]
        response = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        responseBody = json.load(response)
        keyList = responseBody["keys"]
        authKey = None
        for key in keyList:
            if key["kid"] == tokenKid:
               authKey = {
                   "kid": key["kid"],
                   "kty": key["kty"],
                   "use": key["use"],
                   "e": key["e"],
                   "n": key["n"]
               }
        if authKey is None:
            raise AuthError(error={"code":"invalid header", "description": "token could not be found"}, status_code=401)
        payload = jwt.decode(token, key=authKey, algorithms=ALGORITHMS, audience=API_AUDIENCE, issuer="https://"+AUTH0_DOMAIN+"/")
        return payload
    except Exception as e:
        if isinstance(e, AuthError):
            raise AuthError(e.error, e.status_code)
        else:
            raise AuthError(error={"code":"invalid header", "description": "code could not be verified"}, status_code=401)

'''
@Done implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator