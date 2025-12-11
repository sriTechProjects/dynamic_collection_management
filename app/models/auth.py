from pydantic import BaseModel, EmailStr
from typing import Optional

class AdminLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type:str
    org_id: str
    admin_email: str
    
class TokenPayload(BaseModel):
    admin_id: Optional[str] = None
    email: Optional[str] = None
    org_id: Optional[str] = None
    
    