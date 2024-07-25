from aiogram import F
from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database import *
from quiz_data import quiz_data
from utils import get_question, new_quiz

logging.basicConfig(level=logging.INFO)


async def right_answer(callback: types.CallbackQuery):
    logging.info(f"Правильный ответ получен от пользователя: {callback.from_user.id}")

    user_answer = callback.data.split('_')[2]

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    await callback.message.answer(f"Вы выбрали вариант №{user_answer}\nВерно!")

    current_question_index = await get_quiz_index(callback.from_user.id)
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    current_score = await get_current_score(callback.from_user.id)
    current_score += 1

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
        logging.info(f"Сохранение результата (IF) user_id={callback.from_user.id}, score={current_score}")
        await save_result(callback.from_user.id, current_score)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        logging.info(f"Сохранение результата (ELSE) user_id={callback.from_user.id}, score={current_score}")
        await save_result(callback.from_user.id, current_score)
        return current_score


async def wrong_answer(callback: types.CallbackQuery):
    logging.info(f"Неправильный ответ получен от пользователя: {callback.from_user.id}")

    user_answer = callback.data.split('_')[2]

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    await callback.message.answer(
        f"Вы выбрали вариант №{user_answer}\nНеправильно. "
        f"Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    current_score = await get_current_score(callback.from_user.id)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
        await save_result(callback.from_user.id, current_score)
        logging.info(f"Сохранение результата(callback ELSE) user_id={callback.from_user.id}, score={current_score}")
        return current_score  # Пример: Замените на реальный способ получения счета
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await save_result(callback.from_user.id, current_score)
        logging.info(f"Сохранение результата(callback ELSE) user_id={callback.from_user.id}, score={current_score}")
        return current_score


async def save_quiz_result(user_id, score):
    logging.info(f"Сохранение результата: user_id={user_id}, score={score}")
    await save_result(user_id, score)


async def show_statistics(message: types.Message):
    user_id = message.from_user.id
    latest_results = await get_latest_results(user_id)
    if latest_results:
        response = "Последние 10 результатов:\n"
        for score, timestamp in latest_results:
            response += f"Очки: {score}, Дата: {timestamp}\n"

    await message.answer(response)


async def reset_quiz(user_id):
    await update_quiz_index(user_id, 0)
    await save_result(user_id, 0)

def main_menu_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text="Начать игру"))
    keyboard.add(types.KeyboardButton(text="Рейтинговая таблица"))
    return keyboard.as_markup(resize_keyboard=True)


def in_game_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text="Завершить игру"))
    keyboard.add(types.KeyboardButton(text="Рейтинговая таблица"))
    return keyboard.as_markup(resize_keyboard=True)


def after_game_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text="Новая игра"))
    keyboard.add(types.KeyboardButton(text="Рейтинговая таблица"))
    return keyboard.as_markup(resize_keyboard=True)


async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Поехали"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=main_menu_keyboard())


async def cmd_stop(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Поехали"))
    await message.answer("Спасибо что сыграли со мной! До новых встреч!",
                         reply_markup=main_menu_keyboard())


async def cmd_quiz(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Завершить игру"))
    await message.answer(f"Давайте начнем квиз!", reply_markup=main_menu_keyboard())
    await new_quiz(message)


async def cmd_new_game(message: types.Message):
    user_id = message.from_user.id
    await reset_quiz(user_id)
    await message.answer(f"Начнем новую игру!", reply_markup=in_game_keyboard())
    await new_quiz(message)


def register_handlers(dp: Dispatcher):
    dp.callback_query(F.data.startswith("right_answer_"))(right_answer)
    dp.callback_query(F.data.startswith("wrong_answer_"))(wrong_answer)
    dp.message(Command("start"))(cmd_start)
    dp.message(F.text == "Начать игру")(cmd_quiz)
    dp.message(F.text == "Рейтинговая таблица")(show_statistics)
    dp.message(Command("stop"))(cmd_stop)
    dp.message(F.text == "Завершить игру")(cmd_stop)
    dp.message(F.text == "Новая игра")(cmd_new_game)
    dp.message(Command("quiz"))(cmd_quiz)
