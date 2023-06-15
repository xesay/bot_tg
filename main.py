import requests
from config import load_config
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, BaseFilter,Text
from aiogram.types import Message, ContentType
from dataclasses import dataclass
import os
import dotenv
from environs import Env


#загружаем переменные
config = load_config('.env.txt')


#Токен Бота
api: str = config.tg_bot.token

#обьекты бота и диспатчера
bot: Bot = Bot(api)
dp: Dispatcher = Dispatcher()

@dp.message(Command(commands=['start']))
async def start_cmd(message: Message):
    await message.answer('Отправь фото')




if __name__ == '__main__':
    dp.run_polling(bot)
