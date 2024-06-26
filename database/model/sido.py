from ..model import Column, String

from ..model import Base
from ..model import Table

class Sido(Base):
    __tablename__ = Table.sido
    
    orgCd = Column(String(255),index=True, primary_key=True)
    orgdownNm = Column(String(255),index=True)