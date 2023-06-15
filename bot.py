import asyncio
from aiogram import Bot, Dispatcher
from config2 import load_config, Config



async def main() -> None:

    #Загружаем конфиг в переменную среду
    config: Config = load_config('.env.txt')

    #Инифицализируем бот и диспатчер
    bot: Bot = config.tg_bot.token
    dp: Dispatcher = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True) #Пропуск накопившихся апдейтов
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())