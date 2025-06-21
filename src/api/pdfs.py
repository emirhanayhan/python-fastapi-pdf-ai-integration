from fastapi import Request, Depends, UploadFile
from PyPDF2 import PdfReader
from io import BytesIO
import hashlib

from src.utils.auth import authenticate_and_authorize
from src.models.users import UserModel
from src.utils.exceptions import AppException


def init_pdfs_api(app):
    @app.post("/api/v1/pdfs", status_code=201)
    async def create_pdf(request: Request, pdf: UploadFile, user: UserModel = Depends(authenticate_and_authorize)):
        pdf_bytes = await pdf.read()
        pdf_stream = BytesIO(pdf_bytes)
        pdf_reader = PdfReader(pdf_stream)
        texts = "".join([page.extract_text() for page in pdf_reader.pages])
        pdf_hash = hashlib.md5(texts.encode("utf-8")).hexdigest()

        pdf_exists = await request.app.db.files_metadata.find_one({"hash": pdf_hash, "user_id": user.id.hex})
        if pdf_exists:
            raise AppException(
                error_message="pdf already exists",
                error_code="exceptions.pdfAlreadyExists",
                status_code=409
            )

        file_id = await request.app.fs.upload_from_stream(
            pdf.filename, pdf_stream,
            # normally i would store metadata like this
            # but case requirement saying metadata
            # needs to be stored in separate collection
            # metadata={"hash": pdf_hash, "user_id": user.id.hex, "content_type": pdf.content_type}
        )
        file_metadata = await request.app.db.files_metadata.insert_one(
            {
                "hash": pdf_hash, "user_id": user.id.hex,
                "file_name": pdf.filename, "file_id": str(file_id),
                "is_selected": False
            }
        )

        return {"file_id": str(file_id)}

    @app.get("/api/v1/pdfs-list", status_code=200)
    async def get_user_pdfs(request:Request, user: UserModel = Depends(authenticate_and_authorize)):
        user_pdfs = request.app.db.files_metadata.find(
            {"user_id": user.id.hex}, {"file_id": 1}
        )
        ids = [pdf["file_id"] async for pdf in user_pdfs]
        return {"file_ids": ids}

    @app.patch("/api/v1/pdfs/{file_id}")
    async def select_pdf(file_id: str, request: Request, user: UserModel = Depends(authenticate_and_authorize)):
        file_meta = await request.app.db.files_metadata.find_one(
            {"user_id": user.id.hex, "file_id": file_id}
        )
        if file_meta.get("is_selected"):
            raise AppException(
                error_message="pdf already selected",
                error_code="exceptions.pdfAlreadySelected",
                status_code=409
            )
        # ensure single selected
        await request.app.db.files_metadata.update_many(
            {"user_id": user.id.hex}, {'$set': {'is_selected': False}},
        )
        await request.app.db.files_metadata.update_one(
            {"user_id": user.id.hex, "file_id": file_id}, {'$set': {'is_selected': True}}
        )

        return {"selected_pdf": str(file_id)}
