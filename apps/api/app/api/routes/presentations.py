from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.presentation import PresentationCreate, PresentationIR, PresentationUpdate, Slide, SlideCreate, SlideUpdate
from app.services.presentation_service import create_presentation, create_slide, delete_presentation, delete_slide, get_presentation, update_presentation, update_slide

router = APIRouter(tags=["presentations"])


@router.post("/presentations", response_model=PresentationIR, status_code=status.HTTP_201_CREATED)
def create(payload: PresentationCreate, db: Session = Depends(get_db)):
    return create_presentation(db, payload)


@router.get("/presentations/{presentation_id}", response_model=PresentationIR)
def get(presentation_id: UUID, db: Session = Depends(get_db)):
    return get_presentation(db, presentation_id)


@router.patch("/presentations/{presentation_id}", response_model=PresentationIR)
def update(presentation_id: UUID, payload: PresentationUpdate, db: Session = Depends(get_db)):
    return update_presentation(db, presentation_id, payload)


@router.delete("/presentations/{presentation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(presentation_id: UUID, db: Session = Depends(get_db)):
    delete_presentation(db, presentation_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/presentations/{presentation_id}/slides", response_model=Slide, status_code=status.HTTP_201_CREATED)
def add_slide(presentation_id: UUID, payload: SlideCreate, db: Session = Depends(get_db)):
    return create_slide(db, presentation_id, payload)


@router.get("/presentations/{presentation_id}/slides", response_model=list[Slide])
def list_slides(presentation_id: UUID, db: Session = Depends(get_db)):
    return get_presentation(db, presentation_id).slides


@router.patch("/slides/{slide_id}", response_model=Slide)
def edit_slide(slide_id: UUID, payload: SlideUpdate, db: Session = Depends(get_db)):
    return update_slide(db, slide_id, payload)


@router.delete("/slides/{slide_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_slide(slide_id: UUID, db: Session = Depends(get_db)):
    delete_slide(db, slide_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

