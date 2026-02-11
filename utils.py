import re


def toPascalCase(s: str) -> str:
    s = s.strip().lower().replace("-", " ").replace("_", " ")

    return "".join(word.capitalize() for word in s.split())


def toHumanReadableLabel(s: str) -> str:
    s = s.strip().removeprefix("Icon")
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", s)


def toCamelCase(s: str) -> str:
    s = s.strip()

    parts = s.split("-")

    return parts[0] + "".join(word.capitalize() for word in parts[1:])
