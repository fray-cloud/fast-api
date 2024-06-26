from ..model import Column, String

from ..model import Base
from ..model import Table

class Kind(Base):
    __tablename__ = Table.kind
    
    kindCd = Column(String(255),index=True, primary_key=True)
    knm = Column(String(255),index=True)