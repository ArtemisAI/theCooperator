from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        if cls.__name__.endswith("s"):
            return cls.__name__.lower()
        return cls.__name__.lower() + "s"

from .unit import Unit
from .member import Member
from .committee import Committee, CommitteeMemberRole
