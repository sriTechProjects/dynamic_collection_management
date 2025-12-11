# app/main.py
from fastapi import FastAPI
from app.db.session import db
from contextlib import asynccontextmanager
from app.api.v1 import auth, org

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    yield
    db.close()

app = FastAPI(
    title="Organization Management Service",
    version="1.0",
    lifespan=lifespan
)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(org.router, prefix="/org", tags=["Organization"])

@app.get("/")
async def root():
    return {"message": "Service is running", "db_status": "Connected"}