# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import sessionmaker, Session # 해당 방식은 동기 방식.
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession # 비동기 방식.
from dotenv import load_dotenv

from sqlalchemy import text
import asyncio

load_dotenv()
import os
DB_URL =  os.getenv("DB_URL")

if not DB_URL:
    DB_URL = "mysql+aiomysql://manager:qwer1234@mariadb:3306/project"
    # DB_URL = "mysql+aiomysql://manager:qwer1234@localhost:3306/project"
engine = create_async_engine(DB_URL,echo=True)
# SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()

async def get_async_db():
    db = AsyncSession(bind=engine)
    try:
        yield db
    finally:
        await db.close()

async def get_async_test(db = get_async_db()):
    db = await anext(db)
    data = await db.execute(text("SHOW TABLES"))
    print(data.all())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_async_test())
    loop.close()
    
    