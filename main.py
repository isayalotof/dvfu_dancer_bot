import asyncio
# import logging
import os

from aiogram import Bot, Dispatcher
from app import handlers

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


async def main():
    dp.include_router(handlers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")




































