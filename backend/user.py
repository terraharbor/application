from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None
    sha512_hash: str
    token: Optional[str] = None
    token_validity: Optional[int] = None