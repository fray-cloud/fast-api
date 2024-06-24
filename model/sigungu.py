from .default import Union, BaseModel, DefaultIn, DefaultOut, Document, Indexed


class SigunguIn(DefaultIn):
    upr_cd : Union[str, int]

class SigunguOut(Document):
    class Response(DefaultOut.Response):
        class Items(BaseModel):
            class item(BaseModel):
                uprCd : str
                orgCd : str
                orgdownNm : str
            items : dict[str, list[item]]
        body : Items
    response : Response
    
    class Settings:
        name ='sigungu'