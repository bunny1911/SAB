import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from conf import BOT_TOKEN
from handlers.auth import command


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(command.auth_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
