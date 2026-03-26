from pathlib import Path
from pydantic import BaseModel


class ChildElement(BaseModel):
    tag: str
    attrib: dict[str, str]


class Svg(BaseModel):
    name: str
    relative_path: Path = Path(".")
    attrib: dict[str, str]
    ascii: str
    elements: list[ChildElement]
