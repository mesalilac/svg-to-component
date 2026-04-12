from pathlib import Path
from pydantic import BaseModel


class ChildElement(BaseModel):
    tag: str
    attrib: dict[str, str]


class Svg(BaseModel):
    name: str
    relative_path: Path = Path(".")
    original_filename: str
    relative_dir_name: str
    attrib: dict[str, str]
    ascii: str
    elements: list[ChildElement]
