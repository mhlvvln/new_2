from fastapi import APIRouter, UploadFile, Depends, File, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from models import File as FileModel
from database.database import get_db, get_session
from service import verify_token, auth, FileUpload, get_file_info_by_hash

router = APIRouter()

security = HTTPBearer()


@router.get("/protected")
async def protected_route(token: HTTPAuthorizationCredentials = Depends(security)):
    rules = auth(token, ["*"])
    return rules


@router.post("/uploadPhoto")
async def upload_photo(request: Request,
                 token: HTTPAuthorizationCredentials = Depends(security),
                 file: UploadFile = File(...),
                 db: AsyncSession = Depends(get_session)):
    rules = auth(token, ["*"])
    return await FileUpload(db, rules, file, request, "photo")


@router.post("/uploadVideo")
async def upload_photo(request: Request,
                 token: HTTPAuthorizationCredentials = Depends(security),
                 file: UploadFile = File(...),
                 db: AsyncSession = Depends(get_session)):
    rules = auth(token, ["*"])
    return FileUpload(db, rules, file, request, "video")


@router.post("/uploadDocument")
async def upload_photo(request: Request,
                 token: HTTPAuthorizationCredentials = Depends(security),
                 file: UploadFile = File(...),
                 db: AsyncSession = Depends(get_session)):
    rules = auth(token, ["*"])
    return FileUpload(db, rules, file, request, "document")


@router.get("/photos/{hash}")
async def photos(hash: str, db: AsyncSession = Depends(get_session)):
    a = db.execute(select(FileModel).where(FileModel.id > 0))
    return await get_file_info_by_hash(db, hash, "photo")


@router.get("/videos/{hash}")
async def videos(hash: str, db: AsyncSession = Depends(get_session)):
    return await get_file_info_by_hash(db, hash, "video")


@router.get("/documents/{hash}")
async def documents(hash: str, db: AsyncSession = Depends(get_session)):
    return await get_file_info_by_hash(db, hash, "document")