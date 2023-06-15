from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from lexicon import LEXICON_RU
from aiogram import Router


router: Router = Router()

@router.message(CommandStart())
async def proccess_start_command(message: Message):
    await message.answer(LEXICON_RU['/start'])


@router.message(Command(commands=['help']))
async def proccess_help_command(message: Message):
    await message.answer(LEXICON_RU['/help'])