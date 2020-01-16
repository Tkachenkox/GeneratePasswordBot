import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import text, pre
from aiogram.types import ParseMode
import random

API_TOKEN = 'TELEGRAM_API_TOKEN'

logging.basicConfig(level=logging.INFO)

#init bot and dispather
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#decorator for /start command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Bot helpes generate passwords. For more info press /help')

#decorator for /help command
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply('Just send to the bot length of your potential password!')

#main function
@dp.message_handler()
async def generate_p(message: types.Message):
    length = message['text']
    if length.isdigit():
        password = generate(length)
        #format message
        msg = text('Your password - ', pre(password))
        await message.reply(msg, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply('Not correct length')

#generate string
def generate(length):
    if int(length) < 4:
        return 'To short password.'
    check_for_digit = False
    helper_letters = 'qwertyuiopasdfghjklzxcvbnm'
    helper_digits = '1234567890'
    final_str = ''
    while len(final_str) < int(length):
        if random.random() > 0.5:
            if len(final_str) == (int(length) - 1) and check_for_digit == False:
                continue
            ch = random.randint(0, len(helper_letters) - 1)
            if random.random() > 0.5:
                final_str += helper_letters[ch].upper()
            else:
                final_str += helper_letters[ch]
        else:
            check_for_digit = True
            ch = random.randint(0, len(helper_digits) - 1)
            final_str += helper_digits[ch]
    return final_str


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)