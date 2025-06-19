from fastapi import Request
from sqlalchemy.sql import text


def init_healthcheck_api(app):
    @app.get("/api/v1/healthcheck")
    async def healthcheck(request: Request):
        # can be used for kubernetes readiness probe
        # if something is wrong on api or db layer
        # deployment will shown as Unhealthy

        await request.app.db.client.admin.command('ping')
        async with request.app.pg_session() as session:
            await session.execute(text('SELECT 1'))
        return {"status": "healthy"}
