# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # <--- Changed import
import jwt
from app.core.config import settings
from app.models.auth import TokenPayload

# This gives you a simple "Paste Token" box in Swagger
security = HTTPBearer()

async def get_current_admin(token: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # HTTPBearer returns the token object, we need .credentials to get the string
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        org_id: str = payload.get("org_id")
        sub: str = payload.get("sub")
        
        if org_id is None or sub is None:
            raise credentials_exception
            
        return TokenPayload(sub=sub, org_id=org_id, email=payload.get("email"))
    
    except jwt.PyJWTError:
        raise credentials_exception