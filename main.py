import asyncio
# import logging
import os
from aiogram.methods import DeleteWebhook

from aiogram import Bot, Dispatcher
from app import handlers
import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


def clean_database():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Ваш SQL-запрос для очистки базы данных
    cursor.execute("DELETE FROM Place1")  # Укажите имя вашей таблицы
    cursor.execute("DELETE FROM Place2")
    cursor.execute("DELETE FROM Place3")
    cursor.execute("DELETE FROM Place4")
    cursor.execute(f"""UPDATE user
    SET Place1 = 1,
        Place2 = 1,
        Place3 = 1,
        Place4 = 1,
        """)

    conn.commit()
    conn.close()
    print("База данных очищена")


# Создаем и настраиваем планировщик
scheduler = AsyncIOScheduler()
scheduler.add_job(clean_database, 'interval', weeks=1)  # Очищать раз в неделю


async def main():
    scheduler.start()
    dp.include_router(handlers.router)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
