from fastapi import HTTPException, status
from app.db.session import db
from app.core.security import verify_password, create_access_token
from app.models.auth import AdminLogin, Token

class AuthService:
    async def login(self, login_data: AdminLogin)->Token:
        master_db = db.getMasterDB()
        
        admin = await master_db["admins"].find_one({"email":login_data.email})
        
        if not admin:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Incorrect password or email",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        if not verify_password(login_data.password, admin["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect Password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        org_id = str(admin["org_id"])
        
        access_token = create_access_token(
            subject=admin["_id"],
            org_id=org_id,
            email=admin["email"]
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            org_id=org_id,
            admin_email=admin["email"]
        )
            
auth_service = AuthService()