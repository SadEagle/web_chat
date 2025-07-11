from pydantic import BaseModel


class TokenCreate(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
