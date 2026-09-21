from io import BytesIO
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.pptx_renderer import PPTXRenderer
from app.services.presentation_service import get_presentation

router = APIRouter(tags=["exports"])


@router.post("/presentations/{presentation_id}/validate")
def validate(presentation_id: UUID, db: Session = Depends(get_db)):
    return get_presentation(db, presentation_id)


@router.post("/presentations/{presentation_id}/export")
def export(presentation_id: UUID, db: Session = Depends(get_db)):
    presentation = get_presentation(db, presentation_id)
    content = PPTXRenderer().render(presentation)
    filename = f"{presentation.metadata.title.replace(' ', '-')}.pptx"
    return StreamingResponse(BytesIO(content), media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", headers={"Content-Disposition": f'attachment; filename="{filename}"'})

