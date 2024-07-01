from .default import DefaultIn, DefaultOut, BaseModel, Union, dt
from .page import PageIn, PageOut
from odmantic import Model, Field



class SidoIn(DefaultIn, PageIn):
    pass

class SidoOut(BaseModel):
    site_updated : dt.date = dt.date.today()
    class Response(DefaultOut.Response):
        class Items(PageOut):
            class item(BaseModel):
                orgCd : str
                orgdownNm : str
                totalCount : Union[int, None] = None
            items : dict[str, list[item]]
        body : Items
    response : Response

    class Settings:
        name ='sido'
