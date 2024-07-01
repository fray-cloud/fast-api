from sqlalchemy.exc import IntegrityError
from database.model.sido import Sido

from schema.sido import SidoOut

from . import get_async_db, insert, update, select


async def set(sido : SidoOut):
    db = await anext(get_async_db())
    query = insert(Sido).values(sido.response.body.items['item'])
    for sido_data in sido.response.body.items['item']:
        query = insert(Sido).values(orgCd=sido_data.orgCd, orgdownNm=sido_data.orgdownNm)
        try:
            await db.execute(query)
        except IntegrityError:
            await db.close()
        # finally:
        #     query = update(Sido).values(orgCd=sido_data.orgCd, orgdownNm=sido_data.orgdownNm)
        #     await db.execute(query)
    await db.commit()

async def get():
    db = await anext(get_async_db())
    query = select(Sido).order_by(Sido.orgdownNm)
    print(query)
    try:
        data = await db.execute(query)
        data = data.scalars().all()
    except:
        await db.close()
    # await db.commit()
    return data
    

