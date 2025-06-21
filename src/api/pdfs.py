from fastapi import Request, Depends

from src.utils.auth import authenticate_and_authorize


def init_pdfs_api(app):
    @app.post("/api/v1/pdfs")
    async def create_pdf(request: Request, x: None = Depends(authenticate_and_authorize)):
        print()
