import pytest
import json
from pathlib import Path
from jsonschema import Draft202012Validator
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


@pytest.mark.parametrize("payload", [
    {"metadata": {"title": "Missing dimensions"}, "dimensions": {"width": 0, "height": 7.5}},
    {"metadata": {"title": "Bad slide"}, "slides": [{"order": -1}]},
    {"metadata": {"title": "Bad element"}, "slides": [{"elements": [{"type": "unknown", "x": 0, "y": 0, "width": 1, "height": 1}]}]},
])
def test_invalid_ir_payloads_fail_validation(payload):
    with pytest.raises(ValidationError):
        PresentationIR.model_validate(payload)


def test_json_schema_validates_complete_ir_contract():
    schema = json.loads((Path(__file__).parents[3] / "packages/schema/presentation.schema.json").read_text())
    valid = PresentationIR(metadata={"title": "Schema"}, slides=[{"order": 0, "elements": [{"type": "text", "x": 1, "y": 1, "width": 2, "height": 1, "text": "Valid"}]}]).model_dump(mode="json")
    validator = Draft202012Validator(schema)
    assert not list(validator.iter_errors(valid))
    valid["dimensions"]["width"] = 0
    assert list(validator.iter_errors(valid))
