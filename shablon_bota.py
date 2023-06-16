import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command,CommandStart,Text
from aiogram.types import Message, ContentType,ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder



#Токен Бота
api: str = '6190567891:AAHREkg0RnASqvBog6QukChq_AvzLIjv2Lw'

#обьекты бота и диспатчера
bot: Bot = Bot(api)
dp: Dispatcher = Dispatcher()

rules = """
Игроки считают вместе вслух «Камень… Ножницы… Бумага… Раз… Два… Три», \n
одновременно качая кулаками. На счёт «Три» они одновременно показывают при помощи руки один их трёх знаков: 
камень, ножницы или бумагу. Знаки изображены на картинке.\n
Победитель определяется по следующим правилам:\n\n
Камень побеждает ножницы («камень затупляет или ломает ножницы»)
Ножницы побеждают бумагу («ножницы разрезают бумагу»)
Бумага побеждает камень («бумага заворачивает камень»)\n\n
Если игроки показали одинаковый знак, то засчитывается ничья и игра переигрывается.
В классическом варианте в игру играют вдвоём, однако возможна игра большего количества участников. 
При этом ничья засчитывается в ситуации, когда одновременно хотя бы один игрок показал «камень», 
хотя бы один игрок показал «бумагу» и хотя бы один игрок показал «ножницы».Давай сыграем?
"""

html = 'HTML'

kb: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
bt_1: KeyboardButton = KeyboardButton(text='Камень')
bt_2: KeyboardButton = KeyboardButton(text='Ножницы')
bt_3: KeyboardButton = KeyboardButton(text='Бумага')
kb.row(bt_1,bt_2,bt_3)

kb2: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
bt_4: KeyboardButton = KeyboardButton(text='Давай')
bt_5: KeyboardButton = KeyboardButton(text='Не хочу')
kb2.row(bt_4,bt_5)




@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text='Давай сыграем в игру "Камень, Ножницы, Бумага?"\n/help - почитать правила',
    reply_markup=kb2.as_markup(resize_keyboard=True,one_time_keyboard = True))

@dp.message(Command(commands=['help']))
async def cmd_help(message: Message):
    await message.answer(text=f'<b><i>{rules}</i></b>',reply_markup=kb2.as_markup(resize_keyboard = True),parse_mode=html)

@dp.message(Text('Давай'))
async def accept(message: Message):
    await message.answer(text='Отлично! Делай свой выбор!',reply_markup=kb.as_markup(resize_keyboard=True,one_time_keyboard=True))

@dp.message(Text('Не хочу'))
async def no_accept(message: Message):
    await message.answer(text='Хорошо. Если, вдруг, захочешь сыграть - открой клавиатуру и нажми - Давай')

@dp.message(Text(['Бумага', 'Ножницы', 'Камень']))
async def game(message: Message):
    import random
    computer = random.choice(['Ножницы', 'Бумага', 'Камень'])
    if message.text == computer:
        await message.answer(text=f"Оба пользователя выбрали {message.text}. Ничья!!\n"
        f"Давай сыграем еще раз?",reply_markup= kb2.as_markup(resize_keyboard=True,one_time_keyboard = True))
    elif message.text == "Камень":
        if computer == "Ножницы":
            await message.answer(text=f"Камень бьет ножницы! Вы победили!\n"
            f"Давай сыграем еще раз?",reply_markup= kb2.as_markup(resize_keyboard=True,one_time_keyboard = True))
        else:
            await message.answer(text=f"Бумага оборачивает камень! Вы проиграли.\n"
            f"Давай сыграем еще раз?",reply_markup= kb2.as_markup(resize_keyboard=True,one_time_keyboard = True))
    elif message.text == "Бумага":
        if computer == "Камень":
            await message.answer(text=f"Бумага оборачивает камень! Вы победили!\n"
            f"Давай сыграем еще раз?",reply_markup= kb2.as_markup(resize_keyboard=True,one_time_keyboard = True))
        else:
            await message.answer(text=f"Ножницы режут бумагу! Вы проиграли.\n"
            f"Давай сыграем еще раз?",reply_markup= kb2.as_markup(resize_keyboard=True,one_time_keyboard = True))
    elif message.text == "Ножницы":
        if computer == "Бумага":
            await message.answer(text="Ножницы режут бумагу! Вы победили!\n"
            f"Давай сыграем еще раз?",reply_markup= kb2.as_markup(resize_keyboard=True,one_time_keyboard = True))
        else:
            await message.answer(text="Камень бьет ножницы! Вы проиграли.\n"
            f"Давай сыграем еще раз?",reply_markup= kb2.as_markup(resize_keyboard=True,one_time_keyboard = True))



@dp.message()
async def other(message: Message):
    await message.answer(text='Я вас не понимаю',reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    dp.run_polling(bot)
