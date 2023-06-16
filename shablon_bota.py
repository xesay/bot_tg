import requests
from config import TOKEN
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType

#Токен Бота
api: str = TOKEN

#обьекты бота и диспатчера
bot: Bot = Bot(api)
dp: Dispatcher = Dispatcher()


#хэндлер на команду /start
@dp.message(Command(commands=['start']))
async def proccess_start_cmd(message: Message):
    await message.answer('Привет, я эхо бот')


#хэндлер на команду /help
@dp.message(Command(commands=['help']))
async def proccess_help_cmd(message: Message):
    await message.answer('Команды бота')
    #await bot.send_message(chat_id='ID или название чата', text='Какой-то текст')  ДЛЯ ОТПРАВКИ СООБЩЕНИЯ В КАНАЛ


#Хэндлер будет работать на все сообщения
@dp.message()
async def send_echo(message: Message):
    await message.reply(message.text)


@dp.message(F.content_type == ContentType.DOCUMENT)  #хэндлер для контентов (стикеры, доки, фото и тд) либо F.document
async def send_photo_echo(message: Message):
    print(message)
    await message.reply_document(message.document.file_id)



dp.message.register(proccess_start_cmd, Command(commands=['start'])) #Регистрация хэндлера без декоратора


if __name__ == '__main__':
    dp.run_polling(bot)
