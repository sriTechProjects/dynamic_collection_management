from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class OrganizationBase(BaseModel):
    organization_name: str = Field(..., min_length=3, description="Name of organization")
    email: EmailStr = Field(..., description="Admin email address")


class OrganizationCreate(OrganizationBase):
    password: str = Field(..., min_length=8, description="Strong password")

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[@$!%*?&]", v):
            raise ValueError("Password must contain at least one special character (@$!%*?&)")
        return v


class OrganizationUpdate(BaseModel):
    organization_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class OrganizationDelete(BaseModel):
    organization_name: str


class OrganizationResponse(BaseModel):
    organization_name: str
    message: str
    created_at: Optional[datetime] = None
