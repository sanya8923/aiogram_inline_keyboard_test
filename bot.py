import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Text
from aiogram.filters.command import Command, Message
from aiogram.filters.callback_data import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

import config_reader
from random import randint

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config_reader.config.bot_token.get_secret_value())
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: Message):
    kb = [
        [
            KeyboardButton(text='/link'),
            KeyboardButton(text='/random')
        ]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer('Choice button', reply_markup=keyboard)


# builder.row
@dp.message(Command('link'))
async def cmd_link(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='github', url='https://github.com/sanya8923/'))
    builder.row(InlineKeyboardButton(text='nothing', callback_data='nothing_value'))
    await message.answer('Push the button:', reply_markup=builder.as_markup())


# builder.add
@dp.message(Command('random'))
async def cmd_random(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='random', callback_data='random_value'))
    builder.add(InlineKeyboardButton(text='nothing', callback_data='nothing_value'))
    await message.answer('Push button:', reply_markup=builder.as_markup())


@dp.callback_query(Text('random_value'))
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer()


user_data = {}


def get_keyboard():
    button = [
        [
            types.InlineKeyboardButton(text='-1', callback_data='num_decr'),
            types.InlineKeyboardButton(text='+1', callback_data='num_incr')
        ],
        [types.InlineKeyboardButton(text='confirm', callback_data='num_finish')]
    ]
    result = types.InlineKeyboardMarkup(inline_keyboard=button)
    return result


async def update_num_text(message: types.Message, new_value: int):
    if suppress(TelegramBadRequest):  # Страховка от MessageNotModified
        await message.edit_text(
            f'write number: {new_value}',
            reply_markup=get_keyboard()
    )


@dp.message(Command('number'))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer(
        f'Your number: 0',
        reply_markup=get_keyboard()
    )


@dp.callback_query(Text(startswith='num_'))
async def callback_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split('_')[1]

    if action == 'incr':
        user_data[callback.from_user.id] = user_value+1
        await update_num_text(callback.message, user_value+1)
    elif action == 'decr':
        user_data[callback.from_user.id] = user_value-1
        await update_num_text(callback.message, user_value-1)
    elif action == 'finish':
        await callback.message.edit_text(f'total: {user_value}')

    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
