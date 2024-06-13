from .default import DefaultIn, DefaultOut, BaseModel
from .page import PageIn, PageOut
from odmantic import Model, Field

class SidoIn(DefaultIn, PageIn):
    pass

class SidoOut(DefaultOut):
    class Response(DefaultOut.Response):
        class Items(PageOut):
            class item(BaseModel):
                orgCd : str
                orgdownNm : str
            items : dict[str, list[item]]
        body : Items
    response : Response
