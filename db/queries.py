from sqlalchemy import URL, select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from sqlalchemy.orm import sessionmaker

import asyncio

from db.models import TelegramUser


# DONE
async def insert_user(async_sess: async_sessionmaker[AsyncSession], tg_id: int, lang_cd: str, targ_lang_cd: str = "en"):
   async with async_sess() as session:
      async with session.begin():
         try:
            session.add(TelegramUser(
               tg_user=tg_id,
               lang_code=lang_cd,
               targ_lang_code=targ_lang_cd
            ))
         except(IntegrityError):
            pass
         
# DONE
async def update_lang_code(async_sess: async_sessionmaker[AsyncSession], user_id: int, new_lang_cd: str, is_targ_lang: bool = False):
   async with async_sess() as session:
      async with session.begin():
         
         # getting the user
         query = await session.execute(select(TelegramUser).where(TelegramUser.tg_user == user_id))
         user: TelegramUser = query.scalars().one()
         print(user)
         # update the lang_code. The boolean variable "is_targ_lang" will point which lang_code need to replace
         if not is_targ_lang:
            user.lang_code = new_lang_cd
         else:
            user.targ_lang_code = new_lang_cd


async def get_user(async_sess: async_sessionmaker[AsyncSession], user_id: int) -> TelegramUser | None:
   async with async_sess() as session:
      async with session.begin():

         try:
            # getting the user
            query = await session.execute(select(TelegramUser).where(TelegramUser.tg_user == user_id))
            user: TelegramUser = query.scalars().one()
         
         except:
            return None
         
         else:
            return user

""" 
db_url: URL = URL.create(
   drivername = "postgresql+asyncpg",
   username="alex",
   password="alex09",
   host="localhost",
   database="telegram_bot_db"
)
"""


""" async def main():
   # init the async engine for sqlalchemy
   engine = create_async_engine(url=db_url, echo=False)

   # create the async sesson by class factory - async_sessionmaker
   async_session = async_sessionmaker(engine, expire_on_commit=False)

   async with engine.begin() as conn:
      await conn.run_sync(BaseModel.metadata.create_all)

     
   # for AsyncEngine created in function scope, close and
   # clean-up pooled connections
   await engine.dispose()

if __name__ == "__main__":
   asyncio.run(main())

"""
