from sqlmodel import Field, SQLModel, Column, VARCHAR


class TokenCreateModel(SQLModel):
    email: str = Field(sa_column=Column("email", VARCHAR))
    password: str = Field(sa_column=Column("password", VARCHAR))
