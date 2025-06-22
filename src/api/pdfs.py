from bson import ObjectId
from fastapi import Request, Depends, UploadFile
from PyPDF2 import PdfReader
from io import BytesIO
import hashlib

from src.utils.auth import authenticate_and_authorize
from src.utils.exceptions import AppException
from src.models.users import UserModel
from src.models.messages import ChatMessage
from src.models.events import EventModel


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
            pdf.filename,  BytesIO(pdf_bytes),
            metadata={"content_type": pdf.content_type}
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
    async def get_user_pdfs(request: Request, user: UserModel = Depends(authenticate_and_authorize)):
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

    @app.post("/api/v1/pdfs-chat")
    async def pdf_chat(request: Request, user_message:ChatMessage, user: UserModel = Depends(authenticate_and_authorize)):
        file_meta = await request.app.db.files_metadata.find_one(
            {"user_id": user.id.hex, "is_selected": True}
        )
        if not file_meta:
            raise AppException(
                error_message="Selected pdf not found",
                error_code="exceptions.selectedPdfNotFound",
                status_code=404
            )

        grid_out = await request.app.fs.open_download_stream(ObjectId(file_meta["file_id"]))
        pdf_reader = PdfReader(BytesIO(await grid_out.read()))
        content = "".join([page.extract_text() for page in pdf_reader.pages])

        response = await request.app.ai_client.chat.completions.create(
            model=request.app.config["gemini_model"],
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant about user documents"
                               " will be specified as document_text-->[text] user_message-->[message]"},
                {
                    "role": "user",
                    "content": "document_text-->[{}] user_message-->[{}]".format(content, user_message.message)
                }
            ]
        )

        payload = {
            "user_message": user_message.message,
            "ai_response": response.choices[0].message.content,
            "selected_pdf": str(file_meta["file_id"]),
        }
        async with request.app.pg_session() as session:
            event = EventModel(user_id=user.id, document=payload, type="pdf_chat")
            session.add(event)
            await session.commit()
        return payload


