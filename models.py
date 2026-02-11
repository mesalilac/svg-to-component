from pydantic import BaseModel


class ChildElement(BaseModel):
    tag: str
    attrib: dict[str, str]


class Svg(BaseModel):
    name: str
    tsx_relative_path: str | None = None
    attrib: dict[str, str]
    elements: list[ChildElement]
