from pydantic import BaseModel
from typing import Dict, Optional

class User(BaseModel):
    net_id: str
    attributes: Dict = {}

class Token(BaseModel):
    access_token: str
    token_type: str

class CASConfig:
    def __init__(
        self,
        version: str,
        sso_base_url: str,
        #server_base_url: str,
        validate_url: str = "/serviceValidate"
    ):
        self.version = version
        self.sso_base_url = sso_base_url
        #self.server_base_url = server_base_url
        self.validate_url = validate_url

class AuthResponse(BaseModel):
    auth: bool
    user: Optional[User] = None