from fastapi import HTTPException, status
from app.db.session import db
from app.models.orgs import OrganizationCreate, OrganizationResponse, OrganizationUpdate, OrganizationDelete
from app.core.security import get_password_hash
from bson import ObjectId
from datetime import datetime

class OrganizationService:
    async def create_organization(self, data: OrganizationCreate)-> OrganizationResponse:
        master_db = db.getMasterDB()
        
        existing_org = await master_db["organizations"].find_one({"name":data.organization_name})
        if existing_org:
            raise HTTPException(
                status_code=400,
                detail=f"Organization '{data.organization_name}' already exists."
            )
        
        collection_name = f"org_{data.organization_name.lower().replace('', '_')}"
        new_org_id = ObjectId()
        
        org_doc = {
            "_id":new_org_id,
            "name":data.organization_name,
            "collection_name":collection_name,
            "created_at":datetime.utcnow()
        }
        
        hashed_password = get_password_hash(data.password)
        admin_doc = {
            "email":data.email,
            "password_hash":hashed_password,
            "org_id":new_org_id,
            "role":"admin"
        }
        
        try:
            await master_db["organizations"].insert_one(org_doc)
            await master_db["admins"].insert_one(admin_doc)
            
            tenant_collection = db.get_tenant_collection(collection_name)
            await tenant_collection.insert_one({"type": "init_marker", "created_at": datetime.utcnow()})
            
            return OrganizationResponse(
                organization_name=data.organization_name,
                message="Organization and Admin created successfully.",
                created_at=org_doc["created_at"]
            )
            
        except Exception as e:
            await master_db["organizations"].delete_one({"_id": new_org_id})
            await master_db["admins"].delete_one({"org_id": new_org_id})
            raise HTTPException(status_code=500, detail=str(e))
        
    async def get_organization(self, name: str):
        master_db = db.getMasterDB()
        org = await master_db["organizations"].find_one({"name":name})
        
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
        
        return{
            "organization_name":org["name"],
            "collection_name":org["collection_name"],
            "id":str(org["_id"]),
        }    


    async def update_organization(self, org_id: str, data: OrganizationUpdate) -> dict:
        """
        Handles [cite: 30] Update Organization.
        Crucial: If name changes, we must rename the MongoDB collection.
        """
        master_db = db.getMasterDB()
        
        current_org = await master_db["organizations"].find_one({"_id": ObjectId(org_id)})
        if not current_org:
            raise HTTPException(status_code=404, detail="Organization not found")

        update_fields = {}
        
        if data.organization_name and data.organization_name != current_org["name"]:
            if await master_db["organizations"].find_one({"name": data.organization_name}):
                raise HTTPException(status_code=400, detail="Organization name already exists")

            old_collection_name = current_org["collection_name"]
            new_collection_name = f"org_{data.organization_name.lower().replace(' ', '_')}"
            
            try:
                await db.get_tenant_collection(old_collection_name).rename(new_collection_name)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to rename collection: {str(e)}")

            update_fields["name"] = data.organization_name
            update_fields["collection_name"] = new_collection_name

        if data.email:
            await master_db["admins"].update_one(
                {"org_id": ObjectId(org_id)}, 
                {"$set": {"email": data.email}}
            )
        
        if update_fields:
            await master_db["organizations"].update_one(
                {"_id": ObjectId(org_id)}, 
                {"$set": update_fields}
            )
            
        return {"message": "Organization updated successfully", "fields_updated": list(update_fields.keys())}

    async def delete_organization(self, org_id: str):
        """
        Handles [cite: 39] Delete Organization.
        """
        master_db = db.getMasterDB()
        
        org = await master_db["organizations"].find_one({"_id": ObjectId(org_id)})
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
            
        try:
            await db.get_tenant_collection(org["collection_name"]).drop()
        except Exception as e:
            print(f"Warning: Could not drop collection: {e}")

        await master_db["admins"].delete_many({"org_id": ObjectId(org_id)})
        await master_db["organizations"].delete_one({"_id": ObjectId(org_id)})
        
        return {"message": "Organization and data deleted successfully"}
    
    
org_service = OrganizationService() 