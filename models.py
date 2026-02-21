from pydantic import BaseModel


class ChildElement(BaseModel):
    tag: str
    attrib: dict[str, str]


class Svg(BaseModel):
    name: str
    relative_path: str = "."
    attrib: dict[str, str]
    ascii: str
    elements: list[ChildElement]
