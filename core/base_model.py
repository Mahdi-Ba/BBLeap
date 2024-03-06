from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
import re


@as_declarative()
class Base:
    id: Any
    __name__: str

    @classmethod
    def convert_to_snake_case(cls, s: str) -> str:
        # Insert an underscore before each uppercase letter except the first one
        s = re.sub('([A-Z][a-z]+)', r'_\1', s)

        # Convert all uppercase letters to lowercase
        s = s.lower()

        # Remove the leading underscore, if any
        s = s.lstrip('_')

        return s

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.convert_to_snake_case(cls.__name__.lower())
