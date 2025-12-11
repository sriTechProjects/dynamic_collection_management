from fastapi import APIRouter
from app.models.auth import AdminLogin, Token
from app.services.auth_service import auth_service

router = APIRouter()

@router.post("/admin/login", response_model=Token)
async def login(login_data: AdminLogin):
    return await auth_service.login(login_data)