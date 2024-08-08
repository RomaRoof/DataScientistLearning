import logging
import pytz
from datetime import datetime
import aiosqlite

# Зададим имя базы данных
DB_NAME = 'quiz_bot.db'


async def create_table():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                score INTEGER,
                timestamp DATETIME
            )''')
        # Сохраняем изменения
        await db.commit()


async def get_quiz_index(user_id):
    # Подключаемся к базе данных
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def save_result(user_id, score):
    logging.info(f"Сохранено в БАЗУ: user_id={user_id}, score={score}")

    # Получаем текущее время в часовом поясе Екатеринбурга
    ekb_timezone = pytz.timezone('Asia/Yekaterinburg')
    local_time = datetime.now(ekb_timezone).strftime('%Y-%m-%d %H:%M:%S')

    async with aiosqlite.connect(DB_NAME) as db:
        # Проверяем, существует ли запись для данного user_id
        async with db.execute('SELECT 1 FROM results WHERE user_id = ?', (user_id,)) as cursor:
            exists = await cursor.fetchone()

        if exists:
            # Если запись существует, обновляем счет и время
            await db.execute('UPDATE results SET score = ?, timestamp = ? WHERE user_id = ?', (score, local_time, user_id))
        else:
            # Если записи не существует, создаем новую запись
            await db.execute('INSERT INTO results (user_id, score, timestamp) VALUES (?, ?, ?)', (user_id, score, local_time))

        await db.commit()


async def get_current_score(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT score FROM results WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1',
                              (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0

#async def save_result(user_id):
#    async with aiosqlite.connect(DB_NAME) as db:
#        async with db.execute('SELECT score FROM results WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1', (user_id,)) as cursor:
#            result = await cursor.fetchone()
#            if result:
#                current_score = result[0] + 1
#                await db.execute('UPDATE results SET score = ?, timestamp = CURRENT_TIMESTAMP WHERE user_id = ?',
#                                 (current_score, user_id))
#            else:
#                current_score = 1
#                await db.execute('INSERT INTO results (user_id, score, timestamp) VALUES (?, ?, CURRENT_TIMESTAMP)',
#                                 (user_id, current_score))
#        await db.commit()
#        return current_score
#
async def get_latest_results(user_id, limit=10):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT score, timestamp FROM results WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
                              (user_id, limit)) as cursor:
            results = await cursor.fetchall()
            return results


async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()


async def init_db():
    await create_table()
