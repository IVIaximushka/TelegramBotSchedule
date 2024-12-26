import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import common, scenario, stubs
from settings import config


# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv("BOT_TOKEN", config.bot_token.get_secret_value()))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(common.router, scenario.router, stubs.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
