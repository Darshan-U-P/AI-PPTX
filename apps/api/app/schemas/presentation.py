from __future__ import annotations

from typing import Annotated, Literal, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator


Color = Annotated[str, Field(pattern=r"^#?[0-9A-Fa-f]{6}$")]


class Metadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1, max_length=255)
    description: str = ""


class Dimensions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    width: float = Field(default=13.333, gt=0)
    height: float = Field(default=7.5, gt=0)
    unit: Literal["in"] = "in"


class ThemeColors(BaseModel):
    model_config = ConfigDict(extra="forbid")
    background: Color = "#FFFFFF"
    foreground: Color = "#172033"
    primary: Color = "#4F46E5"
    secondary: Color = "#14B8A6"


class ThemeTypography(BaseModel):
    model_config = ConfigDict(extra="forbid")
    heading: str = "Aptos Display"
    body: str = "Aptos"
    caption: str = "Aptos"


class Theme(BaseModel):
    model_config = ConfigDict(extra="forbid")
    colors: ThemeColors = Field(default_factory=ThemeColors)
    typography: ThemeTypography = Field(default_factory=ThemeTypography)
    spacing: float = Field(default=0.25, ge=0)


class BaseElement(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: UUID = Field(default_factory=uuid4)
    x: float = Field(ge=0)
    y: float = Field(ge=0)
    width: float = Field(gt=0)
    height: float = Field(gt=0)
    rotation: float = 0
    opacity: float = Field(default=1, ge=0, le=1)
    z_index: int = 0


class TextElement(BaseElement):
    type: Literal["text"]
    text: str
    font_family: str = "Aptos"
    font_size: float = Field(default=18, gt=0)
    font_weight: int = Field(default=400, ge=100, le=900)
    alignment: Literal["left", "center", "right"] = "left"
    color: Color = "#172033"
    line_height: float = Field(default=1.2, gt=0)


class ImageElement(BaseElement):
    type: Literal["image"]
    source: str = Field(min_length=1)
    fit: Literal["contain", "cover", "fill"] = "contain"
    position: str = "center"
    alt: str = ""


class ShapeElement(BaseElement):
    type: Literal["shape"]
    shape_type: Literal["rectangle", "ellipse", "round_rect"]
    fill: Color = "#4F46E5"
    stroke: Color = "#4F46E5"
    stroke_width: float = Field(default=0, ge=0)
    radius: float = Field(default=0, ge=0)


class LineElement(BaseElement):
    type: Literal["line"]
    color: Color = "#172033"
    stroke_width: float = Field(default=1, ge=0)


class GroupElement(BaseElement):
    type: Literal["group"]
    children: list[dict] = Field(default_factory=list)


Element = Annotated[Union[TextElement, ImageElement, ShapeElement, LineElement, GroupElement], Field(discriminator="type")]


class Slide(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: UUID = Field(default_factory=uuid4)
    layout: str = "blank"
    background: Color = "#FFFFFF"
    elements: list[Element] = Field(default_factory=list)
    speaker_notes: str = ""

    @model_validator(mode="after")
    def unique_element_ids(self):
        if len({element.id for element in self.elements}) != len(self.elements):
            raise ValueError("element IDs must be unique within a slide")
        return self


class Asset(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: UUID = Field(default_factory=uuid4)
    source: str
    alt: str = ""


class PresentationIR(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: UUID = Field(default_factory=uuid4)
    metadata: Metadata
    dimensions: Dimensions = Field(default_factory=Dimensions)
    theme: Theme = Field(default_factory=Theme)
    assets: list[Asset] = Field(default_factory=list)
    slides: list[Slide] = Field(default_factory=list)
    version: int = Field(default=1, ge=1)

    @model_validator(mode="after")
    def unique_slide_ids(self):
        if len({slide.id for slide in self.slides}) != len(self.slides):
            raise ValueError("slide IDs must be unique")
        return self


class PresentationCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = ""


class PresentationUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    theme: Theme | None = None


class SlideCreate(BaseModel):
    layout: str = "blank"
    background: Color = "#FFFFFF"
    elements: list[Element] = Field(default_factory=list)
    speaker_notes: str = ""


class SlideUpdate(BaseModel):
    layout: str | None = None
    background: Color | None = None
    elements: list[Element] | None = None
    speaker_notes: str | None = None

