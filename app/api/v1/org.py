# app/api/v1/org.py
from fastapi import APIRouter, Depends
from app.models.orgs import OrganizationCreate, OrganizationResponse, OrganizationUpdate, OrganizationDelete
from app.services.org_service import org_service
from app.api.deps import get_current_admin
from app.models.auth import TokenPayload 

router = APIRouter()

@router.post("/create", response_model=OrganizationResponse)
async def create_org(org_data: OrganizationCreate):
    return await org_service.create_organization(org_data)

@router.get("/get")
async def get_org(organization_name: str):
    return await org_service.get_organization(organization_name)

@router.put("/update")
async def update_org(
    org_data: OrganizationUpdate, 
    current_admin: TokenPayload = Depends(get_current_admin)
):
    return await org_service.update_organization(current_admin.org_id, org_data)

@router.delete("/delete")
async def delete_org(
    current_admin: TokenPayload = Depends(get_current_admin)
):
    return await org_service.delete_organization(current_admin.org_id)