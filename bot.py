import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis

import redis

from handlers import user_handlers, others_handlers, callback_queries

from config_data.config import TelegramBotConfig, get_bot_config, DataBaseConfig, get_database_config

from keyboards.main_menu import set_main_menu

from db.base import BaseModel

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import URL

from middlewares.db_mddwr import DbSessionMiddleware, RedisInstanceMiddleware



async def main():
    """Main function to run a bot"""
    # get bot config from env
    config_bot: TelegramBotConfig = get_bot_config()
    
    # get database config from env
    config_db: DataBaseConfig = get_database_config()

    db_url: URL = URL.create(
        drivername = config_db.drivername,
        username = config_db.username,
        password = config_db.password,
        host = config_db.host,
        database = config_db.database
    )
    # init the async engine for sqlalchemy
    engine = create_async_engine(url=db_url, echo=False)

    # create the async sesson by class factory - async_sessionmaker
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

     
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    # READ ABOUT dispose() method
    await engine.dispose()

    # # init redis connection
    # redis: Redis = Redis(
    #     host='redis-17415.c281.us-east-1-2.ec2.cloud.redislabs.com',
    #     port=17415,
    #     password="hZFVehKcfayvdSdotzV0BQdGoqBTqZ4z"
    # )
    

    # # init redis storage
    # storage = RedisStorage(redis=redis)

    r = redis.Redis(
    host='localhost',
    port=6379,
    )




    # init the bot with its token
    bot: Bot = Bot(token=config_bot.tg_token, # read about session parameter
                   parse_mode="HTML")


    # init Dispatcher with the storage
    dp: Dispatcher = Dispatcher()


    # await the main menu
    await set_main_menu(bot)


    # Register middleware to work with events: message and callback_query
    dp.message.middleware(DbSessionMiddleware(async_session))
    dp.callback_query.middleware(DbSessionMiddleware(async_session))

    dp.message.middleware(RedisInstanceMiddleware(r))
    dp.callback_query.middleware(RedisInstanceMiddleware(r))

  
    # Register router handlers 
    dp.include_router(user_handlers.router)
    dp.include_router(others_handlers.router)
    dp.include_router(callback_queries.router)


    # we clean our webhook, to not get new updates after restart a bot
    await bot.delete_webhook(drop_pending_updates=True)

    # run a bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())