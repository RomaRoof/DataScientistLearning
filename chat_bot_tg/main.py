import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import API_TOKEN
from database import create_table
from handlers import register_handlers

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=API_TOKEN)
# ДиспетчерФ
dp = Dispatcher()
# Регистрация хендлеров
register_handlers(dp)


# Запуск процесса поллинга новых апдейтов
async def main():
    # Запускаем создание таблицы базы данных
    await create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
