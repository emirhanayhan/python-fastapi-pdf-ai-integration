from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    message: str = Field(description="User message to ai service")
