# app/schemas.py

from pydantic import BaseModel


class BaseItem(BaseModel):
    name: str
    description: str


class CreateSchema(BaseItem):
    pass


class UpdateSchema(BaseItem):
    pass


class ItemSchema(BaseItem):
    id: int

    class Config:
        orm_mode = True
