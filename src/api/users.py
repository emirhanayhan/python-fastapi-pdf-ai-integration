import asyncio
from fastapi import Request
from passlib import hash

from src.models.users import UserModel


def init_users_api(app):
    @app.post("/api/v1/users", status_code=201)
    async def create_user(user: UserModel, request: Request):
        async with request.app.pg_session() as session:
            # safe store password
            hashed_password = await asyncio.wrap_future(
                request.app.thread_pool.submit(hash.bcrypt.hash, user.password)
            )
            user.password = hashed_password

            session.add(user)
            await session.commit()

            # not return hashed password to client
            del user.password

            return user


    # @app.get("/api/v1/users/{user_id}")
    # async def get_user(user_id: str, request: Request):
    #     return {"status": "ok"}
    #
    # @app.put("/api/v1/users/{user_id}")
    # async def update_user(user_id: str, request: Request):
    #     return {"status": "ok"}
    #
    # @app.delete("/api/v1/users/{user_id}")
    # async def delete_user(user_id: str, request: Request):
    #     return {"status": "ok"}
