from enum import StrEnum, auto
from ..config import Base

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Table(StrEnum):
    sido = auto()
    sigungu = auto()
    kind = auto()
    abandonment = auto()


if __name__ == "__main__":
   for table_name in Table:
       print(f"{table_name} is open")


from . import kind, sido, sigungu