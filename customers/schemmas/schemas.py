from typing import Optional
from pydantic import BaseModel


class TokenCreate(BaseModel):
    access_token: str
    token_type: str


class CustomerCreate(BaseModel):
    username: str
    password: Optional[str] = None
    is_active: bool
    is_superuser: bool


class CustomerModify(BaseModel):
    password: Optional[str] = None
    is_active: bool
    is_superuser: bool


class CustomerResponse(BaseModel):
    username: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True
