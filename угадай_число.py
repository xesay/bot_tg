import requests
from config import TOKEN
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, Text
from aiogram.types import Message, ContentType
import random
import datetime
from dataclasses import dataclass


#Токен Бота
api: str = TOKEN

#обьекты бота и диспатчера
bot: Bot = Bot(api)
dp: Dispatcher = Dispatcher()

users: dict = {}

attempts = 5

def getrandomnumber() -> int:
    return random.randint(0, 100)


def my_admin_filter(message: Message) -> bool:
    if message.text == '/admin' and message.from_user.id == 340906161:
        return True
    return False

@dp.message(my_admin_filter)
async def process_start_command(message: Message):
    await message.answer(text='Это команда /admin')
    print(message.from_user)




@dp.message(lambda x: x.text == '/start')
async def cmd_start(message: Message):
    await message.answer(f'Давай сыграем в игру, угадай число?(напишите да или нет)\n/help для помощи\nСегодня {datetime.date.today()}')
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in-game': False,
            'secret-number': None,
            'attempts': None,
            'total-game': 0,
            'wins': 0
            }
    print(users)


@dp.message(Command(commands=['help']))
async def cmd_help(message: Message):
    await message.answer("""
    /start - начать игру\n/cancel - выйти из игры\n/stat - статистика""")


@dp.message(Command(commands=['cancel']))
async def cancel_cmd(message: Message):
    if users[message.from_user.id]['in-game']:
        await message.answer('Вы вышли из игры')
        users[message.from_user.id]['in-game'] = False
    else:
        await message.answer('А мы и так не играем!')

@dp.message(Command(commands=['stat']))
async def cmd_stat(message: Message):
    await message.answer(f'Всего игр сыграно {users[message.from_user.id]["total-game"]}\nИгр выиграно {users[message.from_user.id]["wins"]}')


@dp.message(Text(['Да', 'Давай', 'Сыграем', 'Игра', 'да', 'yes'],ignore_case=True))
async def yes_cmd(message: Message):
    if not users[message.from_user.id]['in-game']:
        await message.answer('Я загадал число от 0 до 100')
        users[message.from_user.id]['in-game'] = True
        users[message.from_user.id]['secret-number'] = getrandomnumber()
        print(users[message.from_user.id]['secret-number'])
        users[message.from_user.id]['attempts'] = attempts
    else:
        await message.answer('Пока мы играем в игру, я могу только реагировать на числа от 0 до 100 и команды /start , /cancel')

    
@dp.message(Text(['нет','Нет','Не хочу', 'Не буду'],ignore_case=True))
async def no_cmd(message: Message):
    if not users[message.from_user.id]['in-game']:
        await message.answer('Жаль, если захотите поиграть, то напишите об этом.')
    else:
        await message.answer('Мы же сейчас с вами играем, пришлите число от 0 до 100.')


@dp.message(lambda x: x.text and x.text.isdigit() and 0 <= int(x.text) <= 100)
async def digit(message: Message):
    print(message.text)
    if users[message.from_user.id]['in-game']:
        if int(message.text) == users[message.from_user.id]['secret-number']:
            await message.answer('Ура, вы выиграли!, Может сыграем еще раз?')
            users[message.from_user.id]['in-game'] = False
            users[message.from_user.id]['total-game'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret-number']:
            await message.answer('Мое число меньше')
            users[message.from_user.id]['attempts'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret-number']:
            await message.answer('Мое число больше')
            users[message.from_user.id]['attempts'] -= 1

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer('К сожалению вы проиграли, хотите сыграть еще раз?, напишите да или нет')
            users[message.from_user.id]['in-game'] = False
            users[message.from_user.id]['total-game'] += 1
    else:
        await message.answer('Мы еще не играем, хотите сыграть еще раз?')


@dp.message()
async def other_text(message: Message):
    if users[message.from_user.id]['in-game']:
        await message.answer('Мы же сейчас с вами играем, пришлите число от 0 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давай просто сыграем в игру, угадай число?, введите /start - для начала игры')


if __name__ == '__main__':
    dp.run_polling(bot)