import logging

from aiogram import F
from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database import get_quiz_index, update_quiz_index
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

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")


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
        f"Вы выбрали вариант №{user_answer}\nНеправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")


async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Поехали"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))


async def cmd_stop(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Поехали"))
    await message.answer("Спасибо что сыграли со мной! До новых встреч!",
                         reply_markup=builder.as_markup(resize_keyboard=True))


async def cmd_quiz(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Завершить игру"))
    await message.answer(f"Давайте начнем квиз!", reply_markup=builder.as_markup(resize_keyboard=True))
    await new_quiz(message)


def register_handlers(dp: Dispatcher):
    dp.callback_query(F.data.startswith("right_answer_"))(right_answer)
    dp.callback_query(F.data.startswith("wrong_answer_"))(wrong_answer)
    dp.message(Command("start"))(cmd_start)
    dp.message(F.text == "Поехали")(cmd_quiz)
    dp.message(Command("stop"))(cmd_stop)
    dp.message(F.text == "Завершить игру")(cmd_stop)
    dp.message(Command("quiz"))(cmd_quiz)
