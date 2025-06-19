from sqlmodel import Field, SQLModel, Column, VARCHAR
from pydantic import EmailStr

from src.models import PkModel, SysModel


class UserModel(SQLModel, PkModel, SysModel, table=True):
    __tablename__ = "users"

    full_name: str = Field(nullable=False)
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True))
    password: str = Field(sa_column=Column("password", VARCHAR))
    role_id: str | None = Field(foreign_key="roles.name")
