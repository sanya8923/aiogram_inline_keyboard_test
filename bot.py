import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

import config_reader

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config_reader.config.bot_token.get_secret_value())
dp = Dispatcher()


# builder.row
@dp.message(Command('start'))
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='github', url='https://github.com/sanya8923/'))
    await message.answer('Push the button:', reply_markup=builder.as_markup())


@


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
