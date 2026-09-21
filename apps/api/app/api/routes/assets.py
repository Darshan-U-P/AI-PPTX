from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.presentation import AssetResponse
from app.services.asset_service import get_asset_file, save_image_asset

router = APIRouter(tags=["assets"])


@router.post("/presentations/{presentation_id}/assets", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def upload_asset(presentation_id: UUID, file: UploadFile = File(...), alt: str = Form(default=""), db: Session = Depends(get_db)):
    return await save_image_asset(db, presentation_id, file, alt)


@router.get("/assets/{asset_id}")
def download_asset(asset_id: UUID, db: Session = Depends(get_db)):
    path, media_type = get_asset_file(db, asset_id)
    return FileResponse(path, media_type=media_type)
