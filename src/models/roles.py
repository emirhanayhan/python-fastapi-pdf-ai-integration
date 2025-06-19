from sqlmodel import Field, SQLModel, JSON, ARRAY, Column, String
from pydantic import EmailStr, field_validator

from src.models import SysModel


class RoleModel(SQLModel, SysModel, table=True):
    __tablename__ = "roles"

    # no need for another uuid based pk just use role name
    # like admin editor engineer etc.
    name: str = Field(nullable=False, unique=True, primary_key=True)
    permissions: ARRAY[str] = Field(sa_column=Column(ARRAY(String)))

    class Config:
        arbitrary_types_allowed = True
