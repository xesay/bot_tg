import asyncio
from aiogram import Bot, Dispatcher
from config2 import load_config, Config
from handlers import other_handlers, user_handlers
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton




async def main() -> None:
    #Загружаем конфиг в переменную среду
    config: Config = load_config('.env.txt')

    #Инифицализируем бот и диспатчер
    bot: Bot = Bot(config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    #рег роутеров в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    #TEST
    await bot.delete_webhook(drop_pending_updates=True) #Пропуск накопившихся апдейтов
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
