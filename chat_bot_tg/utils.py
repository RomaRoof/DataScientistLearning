from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_quiz_index, update_quiz_index
from quiz_data import quiz_data


def generate_options_keyboard(answer_options, correct_option):
    builder = InlineKeyboardBuilder()

    for i, option in enumerate(answer_options):
        callback_data = f"right_answer_{i+1}" if option == correct_option else f"wrong_answer_{i+1}"
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=callback_data)
        )
    builder.adjust(1)
    return builder.as_markup()


async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)


async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)
