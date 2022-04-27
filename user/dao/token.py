from pydantic import BaseModel


class TokenType(BaseModel):
    access_token: str
    token_type: str
