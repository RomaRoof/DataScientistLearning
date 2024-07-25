import logging

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
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
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
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT INTO results (user_id, score) VALUES (?, ?)', (user_id, score))
        await db.commit()


async def get_score(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT score FROM results WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1',
                              (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0


async def get_current_score(user_id):
    return await get_score(user_id)


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
