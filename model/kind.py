from .default import Enum, BaseModel, DefaultIn, DefaultOut, Document


class UpKind(str, Enum):
    all = -1
    dog = 417000
    cat = 422400
    etc = 429900

class KindIn(DefaultIn):
    up_kind_cd : UpKind

class KindOut(Document):
    class Response(DefaultOut.Response):
        class Items(BaseModel):
            class item(BaseModel):
                kindCd : str
                knm : str
            items : dict[str, list[item]]
        body : Items
    response : Response

    class Settings:
        name ='kind'