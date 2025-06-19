from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel, create_engine

from src.api.healthcheck import init_healthcheck
from src.api.users import init_users


@asynccontextmanager
async def lifespan(app):
    db_client = AsyncIOMotorClient(app.config["mongo_connection_string"], retryWrites=True)
    app.db = db_client[app.config["mongo_database_name"]]
    pg_engine = create_async_engine(app.config["postgres_connection_string"])
    app.pg_session = sessionmaker(bind=pg_engine, class_=AsyncSession, expire_on_commit=False)
    if app.config["run_migrations"]:
        from src.models.users import UserModel
        from src.models.roles import RoleModel
        async with pg_engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.create_all)
    yield


def create_fastapi_app(settings):
    app = FastAPI(lifespan=lifespan)
    app.config = settings

    init_healthcheck(app)
    init_users(app)

    return app
