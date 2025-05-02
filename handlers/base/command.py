from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.filters import Command

base_router = Router()


@base_router.callback_query(F.data == "cancel")
async def cancel_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Ви вийшли. Почніть з /start")


@base_router.message(F.text.in_(["❌ Вийти", "Вийти", "/cancel"]))
async def cancel_text(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "❌ Ви вийшли. Почніть з /start", reply_markup=ReplyKeyboardRemove()
    )


@base_router.message(Command("help"))
async def show_help(message: Message):
    await message.answer(
        "🆘 <b>Довідка</b>\n\n"
        "<b>/start</b> — запустити бота\n"
        "<b>/cancel</b> — скасувати поточну дію\n"
        "<b>/help</b> — список доступних команд\n",
        parse_mode="HTML"
    )