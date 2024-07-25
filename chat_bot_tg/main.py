import asyncio
from config import API_TOKEN
from aiogram import Bot, Dispatcher
from handlers import register_handlers
from database import create_table
import logging


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Регистрация хендлеров
register_handlers(dp)


async def main():
    # Запускаем создание таблицы базы данных
    await create_table()
   # await get_user_statistics()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
