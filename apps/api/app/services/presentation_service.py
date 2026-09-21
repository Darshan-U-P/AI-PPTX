from uuid import UUID

from sqlalchemy.orm import Session

from app.models.presentation import PresentationRecord, PresentationVersionRecord
from app.schemas.presentation import PresentationCreate, PresentationIR, PresentationUpdate, Slide, SlideCreate, SlideUpdate


class NotFoundError(Exception):
    pass


def create_presentation(db: Session, payload: PresentationCreate) -> PresentationIR:
    ir = PresentationIR(metadata={"title": payload.title, "description": payload.description})
    record = PresentationRecord(id=str(ir.id), title=payload.title, ir=ir.model_dump(mode="json"), version=ir.version)
    db.add(record)
    db.add(PresentationVersionRecord(presentation_id=str(ir.id), version=ir.version, ir=ir.model_dump(mode="json")))
    db.commit()
    return ir


def list_presentations(db: Session) -> list[PresentationIR]:
    return [PresentationIR.model_validate(record.ir) for record in db.query(PresentationRecord).order_by(PresentationRecord.updated_at.desc()).all()]


def get_presentation(db: Session, presentation_id: UUID) -> PresentationIR:
    record = db.get(PresentationRecord, str(presentation_id))
    if not record:
        raise NotFoundError("Presentation not found")
    return PresentationIR.model_validate(record.ir)


def save_presentation(db: Session, presentation: PresentationIR) -> PresentationIR:
    record = db.get(PresentationRecord, str(presentation.id))
    if not record:
        raise NotFoundError("Presentation not found")
    presentation.version = record.version + 1
    record.title = presentation.metadata.title
    record.version = presentation.version
    record.ir = presentation.model_dump(mode="json")
    db.add(PresentationVersionRecord(presentation_id=str(presentation.id), version=presentation.version, ir=record.ir))
    db.commit()
    return presentation


def update_presentation(db: Session, presentation_id: UUID, payload: PresentationUpdate) -> PresentationIR:
    presentation = get_presentation(db, presentation_id)
    if payload.title is not None:
        presentation.metadata.title = payload.title
    if payload.description is not None:
        presentation.metadata.description = payload.description
    if payload.theme is not None:
        presentation.theme = payload.theme
    return save_presentation(db, presentation)


def delete_presentation(db: Session, presentation_id: UUID) -> None:
    record = db.get(PresentationRecord, str(presentation_id))
    if not record:
        raise NotFoundError("Presentation not found")
    db.delete(record)
    db.commit()


def create_slide(db: Session, presentation_id: UUID, payload: SlideCreate) -> Slide:
    presentation = get_presentation(db, presentation_id)
    insert_at = payload.order if payload.order is not None else len(presentation.slides)
    slide = Slide(**payload.model_dump(exclude={"order"}), order=insert_at)
    presentation.slides.insert(min(insert_at, len(presentation.slides)), slide)
    _normalize_slide_order(presentation)
    save_presentation(db, presentation)
    return slide


def update_slide(db: Session, slide_id: UUID, payload: SlideUpdate) -> Slide:
    record = next((item for item in db.query(PresentationRecord).all() if any(str(slide["id"]) == str(slide_id) for slide in item.ir.get("slides", []))), None)
    if not record:
        raise NotFoundError("Slide not found")
    presentation = PresentationIR.model_validate(record.ir)
    slide = next(slide for slide in presentation.slides if slide.id == slide_id)
    for field in payload.model_fields_set:
        setattr(slide, field, getattr(payload, field))
    if "order" in payload.model_fields_set and payload.order is not None:
        presentation.slides.remove(slide)
        presentation.slides.insert(min(payload.order, len(presentation.slides)), slide)
        _normalize_slide_order(presentation)
    presentation = save_presentation(db, presentation)
    return next(item for item in presentation.slides if item.id == slide_id)


def delete_slide(db: Session, slide_id: UUID) -> None:
    record = next((item for item in db.query(PresentationRecord).all() if any(str(slide["id"]) == str(slide_id) for slide in item.ir.get("slides", []))), None)
    if not record:
        raise NotFoundError("Slide not found")
    presentation = PresentationIR.model_validate(record.ir)
    presentation.slides = [slide for slide in presentation.slides if slide.id != slide_id]
    _normalize_slide_order(presentation)
    save_presentation(db, presentation)


def _normalize_slide_order(presentation: PresentationIR) -> None:
    presentation.slides.sort(key=lambda item: item.order)
    for order, slide in enumerate(presentation.slides):
        slide.order = order
