import requests
from config import TOKEN
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, Text
from aiogram.types import Message, ContentType
import random

#Токен Бота
api: str = TOKEN

#обьекты бота и диспатчера
bot: Bot = Bot(api)
dp: Dispatcher = Dispatcher()

user: dict = {
    'in-game': False,
    'secret-number': None,
    'attempts': None,
    'total-game': 0,
    'wins': 0
}

attempts = 5

def getrandomnumber() -> int:
    return random.randint(0, 100)


@dp.message(Command(commands=['start']))
async def cmd_start(message: Message):
    await message.answer('Давай сыграем в игру, угадай число?(напишите да или нет)\n/help для помощи')


@dp.message(Command(commands=['help']))
async def cmd_help(message: Message):
    await message.answer("""
    /start - начать игру\n/cancel - выйти из игры\n/stat - статистика""")


@dp.message(Command(commands=['cancel']))
async def cancel_cmd(message: Message):
    if user['in-game']:
        await message.answer('Вы вышли из игры, если хотите сыграть снова - напишите об этом')
        user['in-game'] = False
    else:
        await message.answer('Мы и так не играем, может сыграем разок?')


@dp.message(Text(['Да', 'Давай', 'Сыграем', 'Игра', 'да', 'yes'],ignore_case=True))
async def yes_cmd(message: Message):
    if not user['in-game']:
        await message.answer('Я загадал число от 0 до 100')
        user['in-game'] = True
        user['secret-number'] = getrandomnumber()
        print(user['secret-number'])
        user['attempts'] = attempts
    else:
        await message.answer('Пока мы играем в игру, я могу только реагировать на числа от 0 до 100 и команды /start , /cancel')

    
@dp.message(Text(['нет','Нет','Не хочу', 'Не буду'],ignore_case=True))
async def no_cmd(message: Message):
    if not user['in-game']:
        await message.answer('Жаль, если захотите поиграть, то напишите об этом.')
    else:
        await message.answer('Мы же сейчас с вами играем, пришлите число от 0 до 100.')


@dp.message(lambda x: x.text and x.text.isdigit() and 0 <= int(x.text) <= 100)
async def digit(message: Message):
    print(message.text)
    if user['in-game']:
        if int(message.text) == user['secret-number']:
            await message.answer('Ура, вы выиграли!, Может сыграем еще раз?')
            user['in-game'] = False
            user['total-game'] += 1
            user['wins'] += 1
        elif int(message.text) > user['secret-number']:
            await message.answer('Мое число меньше')
            user['attempts'] -= 1
        elif int(message.text) < user['secret-number']:
            await message.answer('Мое число больше')
            user['attempts'] -= 1

        if user['attempts'] == 0:
            await message.answer('К сожалению вы проиграли, хотите сыграть еще раз?, напишите да или нет')
            user['in-game'] = False
            user['total-game'] += 1
    else:
        await message.answer('Мы еще не играем, хотите сыграть еще раз?')


@dp.message()
async def other_text(message: Message):
    if user['in-game']:
        await message.answer('Мы же сейчас с вами играем, пришлите число от 0 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давай просто сыграем в игру, угадай число?, введите /start - для начала игры')


if __name__ == '__main__':
    dp.run_polling(bot)