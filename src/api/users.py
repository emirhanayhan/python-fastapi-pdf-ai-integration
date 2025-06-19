from fastapi import Request


def init_users(app):
    @app.post("/api/v1/users")
    async def create_user(request: Request):
        return {"status": "ok"}

    @app.get("/api/v1/users/{user_id}")
    async def get_user(user_id: str, request: Request):
        return {"status": "ok"}

    @app.put("/api/v1/users/{user_id}")
    async def update_user(user_id: str, request: Request):
        return {"status": "ok"}

    @app.delete("/api/v1/users/{user_id}")
    async def delete_user(user_id: str, request: Request):
        return {"status": "ok"}
