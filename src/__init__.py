from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from concurrent.futures import ThreadPoolExecutor

from src.api.healthcheck import init_healthcheck_api
from src.api.users import init_users_api
from src.api.tokens import init_tokens_api
from src.utils.exceptions import AppException


@asynccontextmanager
async def lifespan(app):
    # init mongo client
    db_client = AsyncIOMotorClient(app.config["mongo_connection_string"], retryWrites=True)
    app.db = db_client[app.config["mongo_database_name"]]

    # init postgres client
    pg_engine = create_async_engine(app.config["postgres_connection_string"])
    app.pg_session = sessionmaker(bind=pg_engine, class_=AsyncSession, expire_on_commit=False)

    # run migrations if option --migrate=true given
    if app.config["run_migrations"]:
        from src.models.users import UserModel
        from src.models.roles import RoleModel
        async with pg_engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.create_all)

    # for cpu bound tasks to not block api
    # not forget the use it with asyncio.wrap_future
    # otherwise still blocks event loop
    app.thread_pool = ThreadPoolExecutor()

    yield


def init_exception_handler(app):
    @app.exception_handler(Exception)
    async def exception_handler(rq, exc: Exception):
        if isinstance(exc, AppException):
            return JSONResponse(
                status_code=exc.status_code,
                content={"error_msg": exc.error_message, "error_code": exc.error_code}
            )
        return JSONResponse(
            status_code=500,
            content={
                "error_msg": "internal server error {}".format(type(exc).__name__),
                "error_code": "exceptions.internalServerError"
            }
        )


def create_fastapi_app(settings):
    app = FastAPI(lifespan=lifespan)
    app.config = settings

    init_exception_handler(app)

    # init apis
    init_healthcheck_api(app)
    init_users_api(app)
    init_tokens_api(app)

    return app
