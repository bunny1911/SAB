from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.auth.buttom import auth_buttons

auth_router = Router()


@auth_router.message(F.text == "/start")
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    text = (
        "👋 Привіт! Це бот агентства нерухомості «Бульвар».\n\n"
        "Він дозволяє ріелторам створювати оголошення для публікації в Telegram-каналі.\n\n"
        "Оберіть дію:"
    )
    await message.answer(text, reply_markup=auth_buttons)
