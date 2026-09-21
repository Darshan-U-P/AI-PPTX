import pytest
from pydantic import ValidationError

from app.schemas.presentation import PresentationIR


def test_valid_presentation_ir_passes():
    ir = PresentationIR(metadata={"title": "Quarterly review"}, slides=[{"elements": [{"type": "text", "x": 1, "y": 1, "width": 3, "height": 1, "text": "Hello"}]}])
    assert ir.slides[0].elements[0].type == "text"


def test_invalid_element_fails_validation():
    with pytest.raises(ValidationError):
        PresentationIR(metadata={"title": "Invalid"}, slides=[{"elements": [{"type": "shape", "x": -1, "y": 1, "width": 3, "height": 1, "shape_type": "rectangle"}]}])


def test_duplicate_element_ids_fail_validation():
    item = {"id": "c53af4db-99d1-4d9a-a17e-111111111111", "type": "text", "x": 1, "y": 1, "width": 3, "height": 1, "text": "Hello"}
    with pytest.raises(ValidationError, match="unique"):
        PresentationIR(metadata={"title": "Invalid"}, slides=[{"elements": [item, item]}])

