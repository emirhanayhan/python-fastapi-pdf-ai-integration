import jwt
from fastapi import Request
from sqlmodel import select

from src.utils.exceptions import AppException
from src.models.users import UserModel
from src.models.roles import RoleModel


async def authenticate_and_authorize(rq: Request):
    # TODO add wildcard logic

    # action like create_pdf
    # permission --> api.create_pdf
    # required permission to access this endpoint
    required_permission = "api." + rq.scope["route"].name

    if not rq.headers.get("authorization").startswith("Bearer "):
        raise AppException(
            error_message="invalid authorization header",
            error_code="exceptions.invalidAuthorizationHeader",
            status_code=401
        )

    token = rq.headers.get("authorization").split("Bearer ")[1]

    decoded = jwt.decode(token, algorithms="HS256", options={"verify_signature": False})
    if decoded.get("tp") != "ac":
        raise AppException(
            error_message="invalid token type",
            error_code="exceptions.invalidTokenType",
            status_code=401
        )
    async with rq.app.pg_session() as session:
        user, role = (await session.exec(select(UserModel, RoleModel).join(RoleModel).where(UserModel.id == decoded["den"]))).first()
        if not user:
            raise AppException(
                error_message="User not found",
                error_code="exceptions.userNotFound",
                status_code=404
            )
    verified_decoded = jwt.decode(token, key=user.password, algorithms="HS256", options={"verify_signature": True, "verify_exp": True})
    if required_permission not in role.permissions:
        raise AppException(
            error_message="User has no permission take this action",
            error_code="exceptions.userNotAuthorized",
            status_code=403
        )
