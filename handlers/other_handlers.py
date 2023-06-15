from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from lexicon import LEXICON_RU
from aiogram import Router


router: Router = Router()


@router.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(message.chat.id)
    except TypeError:
        await message.reply(LEXICON_RU['no_echo'])