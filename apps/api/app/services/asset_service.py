from pathlib import Path
from uuid import UUID, uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import assets_path
from app.models.presentation import AssetRecord
from app.schemas.presentation import Asset, AssetResponse
from app.services.presentation_service import NotFoundError, get_presentation, save_presentation

ALLOWED_IMAGE_TYPES = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif", "image/webp": ".webp"}


class AssetValidationError(Exception):
    pass


async def save_image_asset(db: Session, presentation_id: UUID, upload: UploadFile, alt: str = "") -> AssetResponse:
    if upload.content_type not in ALLOWED_IMAGE_TYPES:
        raise AssetValidationError("Only PNG, JPEG, GIF, and WebP image uploads are supported")
    presentation = get_presentation(db, presentation_id)
    asset_id = uuid4()
    filename = f"{asset_id}{ALLOWED_IMAGE_TYPES[upload.content_type]}"
    destination = assets_path() / filename
    content = await upload.read()
    if not content:
        raise AssetValidationError("Uploaded image is empty")
    if len(content) > 10 * 1024 * 1024:
        raise AssetValidationError("Uploaded image exceeds the 10 MB limit")
    destination.write_bytes(content)
    source = f"asset://{filename}"
    db.add(AssetRecord(id=str(asset_id), presentation_id=str(presentation_id), source=source, alt=alt, media_type=upload.content_type))
    presentation.assets.append(Asset(id=asset_id, source=source, alt=alt))
    save_presentation(db, presentation)
    return AssetResponse(id=asset_id, source=source, alt=alt, media_type=upload.content_type)


def get_asset_file(db: Session, asset_id: UUID) -> tuple[Path, str]:
    asset = db.get(AssetRecord, str(asset_id))
    if not asset:
        raise NotFoundError("Asset not found")
    filename = asset.source.removeprefix("asset://")
    path = assets_path() / Path(filename).name
    if not path.is_file():
        raise NotFoundError("Asset file not found")
    return path, asset.media_type
