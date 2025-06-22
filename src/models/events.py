from sqlmodel import Field, SQLModel, Column, JSON
from pydantic import EmailStr
from uuid import UUID
from src.models import PkModel, SysModel


class EventModel(SQLModel, PkModel, SysModel, table=True):
    # TODO implement events for all actions
    __tablename__ = "events"

    user_id: UUID = Field(foreign_key="users.id")
    type: str = Field(nullable=False)
    document: dict = Field(default_factory=dict, sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True
