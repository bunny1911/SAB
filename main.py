import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from conf import BOT_TOKEN
from handlers.auth import command as auth_command
from handlers.base import command as base_command
from handlers.base.command import help_commands


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(help_commands)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(base_command.base_router)
    dp.include_router(auth_command.auth_router)
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
