from datetime import datetime, timedelta
from typing import Any, Union
import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plainPassword: str, hashedPassword: str) -> bool:
    return pwd_context.verify(plainPassword, hashedPassword)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], org_id: str, email: str) -> str:
    """
    Creates a JWT string signed with our SECRET_KEY.
    Assignment Requirement: "Implement admin login using JWT" 
    """
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # We embed the critical routing info into the token payload
    to_encode = {
        "exp": expire,          # Expiration time
        "sub": str(subject),    # Subject (Admin ID)
        "org_id": str(org_id),  # Organization ID (For routing)
        "email": email
    }
    
    # Generate the token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt