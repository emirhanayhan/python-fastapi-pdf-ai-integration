import jwt
import uuid
from datetime import datetime, timedelta


def generate_jwt_token(user_id, secret, access_token_ttl, refresh_token_ttl):
    jwt_payload = {
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(seconds=access_token_ttl),
        # can be used in future for single use jwt
        "jti": str(uuid.uuid4().hex),
        # identifier
        "den": str(user_id),
        # type --> access token
        "tp": "ac",
    }
    # generate access token
    access_token = jwt.encode(payload=jwt_payload, key=secret, algorithm='HS256')

    # update expire and type to refresh token
    jwt_payload.update({"tp": "rf", "exp": datetime.utcnow() + timedelta(seconds=refresh_token_ttl)})
    # generate refresh token
    refresh_token = jwt.encode(jwt_payload, key=secret, algorithm='HS256')

    return access_token, refresh_token
