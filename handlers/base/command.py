from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, Message, ReplyKeyboardRemove

from handlers.auth.keyboard import auth_keyboard


# Defined base router
base_router = Router()

# Defined help commands
help_commands = [
    BotCommand(command="start", description="Почати роботу з ботом"),
    BotCommand(command="cancel", description="Скасувати поточну дію"),
    BotCommand(command="help", description="Інструкція та підтримка"),
]


@base_router.message(F.text == "/start")
async def start_command(message: Message, state: FSMContext):
    """
    Handles the /start command.

    Clears the current FSM state and sends a welcome message with action options:
    login, register, or exit.
    """

    # Clear state
    await state.clear()

    # Defined start text
    text = (
        "👋 Привіт! Це бот агентства нерухомості «Бульвар».\n\n"
        "Він дозволяє ріелторам створювати оголошення для публікації в Telegram-каналі.\n\n"
        "Оберіть дію:"
    )

    # Send message
    await message.answer(text, reply_markup=auth_keyboard)


@base_router.message(F.text.in_(["❌ Вийти", "Вийти", "/cancel"]))
async def cancel_text(message: Message, state: FSMContext):
    """
    Handles user exit actions.

    Clears the current FSM state, removes the keyboard, and suggests restarting with /start.
    """

    # Clear state
    await state.clear()

    # Defined exit text
    text = "❌ Ви вийшли. Почніть з /start"

    # Send message
    await message.answer(
        text, reply_markup=ReplyKeyboardRemove()
    )


@base_router.message(Command("help"))
async def show_help(message: Message):
    """
    Handles the /help command.

    Displays a list of available bot commands and their descriptions.
    """

    # Defined help text
    text = (
        "🆘 <b>Довідка</b>\n\n"
        "<b>/start</b> — запустити бота\n"
        "<b>/cancel</b> — скасувати поточну дію\n"
        "<b>/help</b> — список доступних команд\n",
    )

    # Send message
    await message.answer(
        text,
        parse_mode="HTML"
    )
