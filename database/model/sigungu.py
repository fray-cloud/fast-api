from ..model import Column, ForeignKey, String

from ..model import Base
from ..model import Table

class Sigungu(Base):
    __tablename__ = Table.sigungu
    
    orgCd = Column(String(255),index=True, primary_key=True)
    uprCd = Column(String(255), ForeignKey(column=f"{Table.sido}.orgCd"), index=True)
    orgdownNm = Column(String(255),index=True)