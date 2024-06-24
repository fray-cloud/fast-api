from .sido import SidoIn, SidoOut
from .sigungu import SigunguIn, SigunguOut
from .kind import KindIn, KindOut
from .abandonment_public import AbandonmentIn, AbandonmentOut

# motor - MongoDB 용 비동기 python 라이브러리
from motor.motor_asyncio import AsyncIOMotorClient
# from odmantic import AIOEngine
from beanie import init_beanie, PydanticObjectId

# 소중한 Secrets.json 가져오기
from .config import MONGO_DB_NAME, MONGO_DB_URL

test_json = {
    "response": {
        "header": {
            "reqNo": 274613603,
            "resultCode": "00",
            "resultMsg": "NORMAL SERVICE.",
            "errorMsg": "null"
        },
        "body": {
            "numOfRows": 30,
            "pageNo": 1,
            "totalCount": 17,
            "items": {
                "item": [
                    {
                        "orgCd": "6110000",
                        "orgdownNm": "서울특별시"
                    },
                    {
                        "orgCd": "6260000",
                        "orgdownNm": "부산광역시"
                    },
                    {
                        "orgCd": "6270000",
                        "orgdownNm": "대구광역시"
                    },
                    {
                        "orgCd": "6280000",
                        "orgdownNm": "인천광역시"
                    },
                    {
                        "orgCd": "6290000",
                        "orgdownNm": "광주광역시"
                    },
                    {
                        "orgCd": "5690000",
                        "orgdownNm": "세종특별자치시"
                    },
                    {
                        "orgCd": "6300000",
                        "orgdownNm": "대전광역시"
                    },
                    {
                        "orgCd": "6310000",
                        "orgdownNm": "울산광역시"
                    },
                    {
                        "orgCd": "6410000",
                        "orgdownNm": "경기도"
                    },
                    {
                        "orgCd": "6530000",
                        "orgdownNm": "강원특별자치도"
                    },
                    {
                        "orgCd": "6430000",
                        "orgdownNm": "충청북도"
                    },
                    {
                        "orgCd": "6440000",
                        "orgdownNm": "충청남도"
                    },
                    {
                        "orgCd": "6540000",
                        "orgdownNm": "전북특별자치도"
                    },
                    {
                        "orgCd": "6460000",
                        "orgdownNm": "전라남도"
                    },
                    {
                        "orgCd": "6470000",
                        "orgdownNm": "경상북도"
                    },
                    {
                        "orgCd": "6480000",
                        "orgdownNm": "경상남도"
                    },
                    {
                        "orgCd": "6500000",
                        "orgdownNm": "제주특별자치도"
                    }
                ]
            }
        }
    }
}

class MongoDB:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_DB_URL)

    async def connect(self):
        await init_beanie(database=self.client[MONGO_DB_NAME], document_models=[SidoOut, SigunguOut, KindOut, AbandonmentOut])
        print("DB 와 연결되었습니다.왜 안돼") 
        print(SidoOut(**test_json))
        # print(SigunguOut)
        # test = await SidoOut.find_one({'$text' : {"$search" : '제주특별자치도'}})
        # if test is not None :
        #     for t in test:
        #         print(t)
        

    
    def close(self):
        self.client.close()

mongodb = MongoDB()