from aiogram.types import Message,ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton,KeyboardButtonPollType,WebAppInfo
from aiogram.filters import Command, CommandStart,Text
from lexicon import LEXICON_RU
from aiogram import Router
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router: Router = Router()

# Создаем кнопку
web_app_btn: KeyboardButton = KeyboardButton(
                                text='Start Web App',
                                web_app=WebAppInfo(url="https://youtube.com"))

# Создаем объект клавиатуры
web_app_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                            keyboard=[[web_app_btn]],
                                            resize_keyboard=True)
@router.message(CommandStart())
async def proccess_start_command(message: Message):
    await message.answer(LEXICON_RU['/start'],reply_markup=web_app_keyboard)
    print(message.text)


@router.message(Command(commands=['help']))
async def proccess_help_command(message: Message):
    await message.answer(LEXICON_RU['/help'])

