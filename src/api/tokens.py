import asyncio
from fastapi import Request
from sqlmodel import select
from passlib.hash import bcrypt

from src.models.tokens import TokenCreateModel
from src.models.users import UserModel
from src.utils.exceptions import AppException
from src.utils.jwt_helpers import generate_jwt_token


def init_tokens_api(app):
    @app.post("/api/v1/tokens", status_code=201)
    async def create_token(credentials: TokenCreateModel, request: Request):
        async with request.app.pg_session() as session:
            user = (await session.exec(select(UserModel).where(UserModel.email == credentials.email))).first()
            if not user:
                raise AppException(
                    error_message="Email or password missmatch",
                    error_code="exceptions.emailOrPasswordMissmatch",
                    status_code=403
                )
        verified = await asyncio.wrap_future(
            request.app.thread_pool.submit(bcrypt.verify, credentials.password, user.password)
        )
        if not verified:
            raise AppException(
                error_message="Email or password missmatch",
                error_code="exceptions.emailOrPasswordMissmatch",
                status_code=403
            )
        # TODO this started to look ugly
        ac_token, rf_token = await asyncio.wrap_future(
            request.app.thread_pool.submit(
                generate_jwt_token, str(user.id.hex), user.password,
                request.app.config["access_token_ttl"],
                request.app.config["refresh_token_ttl"],
            )
        )

        return {"user_id": user.id, "access_token": ac_token, "refresh_token": rf_token}
