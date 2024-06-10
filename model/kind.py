from .default import Enum, BaseModel, DefaultIn, DefaultOut

class UpKind(str, Enum):
    dog = 417000
    cat = 422400
    etc = 429900

class KindIn(DefaultIn):
    up_kind_cd : UpKind

class KindOut(DefaultOut):
    class Response(DefaultOut.Response):
        class Items(BaseModel):
            class item(BaseModel):
                kindCd : str
                knm : str
            items : dict[str, list[item]]
        body : Items
    response : Response