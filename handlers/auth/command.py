from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select

from conf import REALTOR_PASSWORD
from db.base import get_session
from db.models.realtor import Realtor
from handlers.auth.keyboard import (
    add_listing_keyboard,
    back_keyboard,
    register_keyboard,
    send_phone_keyboard
)
from handlers.auth.state import UserState


# Defined auth router
auth_router = Router()


@auth_router.message(F.text == "📝 Зареєструватися")
async def handle_register_click(message: Message, state: FSMContext):
    """
    Initiates registration by checking if the user is already registered.
    """

    # Set default value
    realtor = None

    # Get realtor from DB
    async for session in get_session():
        realtor_query = await session.execute(
            select(Realtor).where(Realtor.telegram_id == message.from_user.id)
        )
        realtor = realtor_query.scalar_one_or_none()

    if realtor:
        # Found
        await message.answer("Ви вже зареєстровані!", show_alert=True)
        return

    # Send message
    await message.answer("Надішліть пароль для реєстрації:", reply_markup=back_keyboard)
    await state.set_state(UserState.step_password)


@auth_router.message(F.text == "🔐 Увійти")
async def handle_login(message: Message, state: FSMContext):
    """
    Logs the user in if already registered.
    """

    # Set default value
    realtor = None

    # Get  realtor from DB
    async for session in get_session():
        realtor_query = await session.execute(
            select(Realtor).where(Realtor.telegram_id == message.from_user.id)
        )
        realtor = realtor_query.scalar_one_or_none()

    if not realtor:
        # Not found
        await message.answer(
            "❗️ Вас ще не зареєстровано. Спочатку пройдіть реєстрацію.",
            reply_markup=register_keyboard,
        )
        return

    # Send message
    await message.answer(
        "✅ Ви увійшли успішно.", reply_markup=add_listing_keyboard
    )
    await state.clear()


@auth_router.message(UserState.step_password)
async def check_password(message: Message, state: FSMContext):
    """
    Handles password check before continuing registration.
    """

    if message.text == "Назад":
        # Exist
        await message.answer("⛔️ Ви вже на початку реєстрації.", reply_markup=back_keyboard)
        return

    if message.text != REALTOR_PASSWORD:
        # Not valid password
        await message.answer("❌ Невірний пароль. Спробуйте ще раз:", reply_markup=back_keyboard)
        return

    # Set state and send message
    await state.set_state(UserState.step_first_name)
    await message.answer("✅ Пароль підтверджено. Введіть ваше імʼя:", reply_markup=back_keyboard)


@auth_router.message(UserState.step_first_name)
async def ask_last_name(message: Message, state: FSMContext):
    """
    Collects first name or returns to password step.
    """

    if message.text == "Назад":
        # Exist => update
        await state.update_data(going_back=True)
        await state.set_state(UserState.step_password)
        await message.answer("⬅️ Введіть пароль ще раз:", reply_markup=back_keyboard)
        return

    # Set/update state and send message
    await state.update_data(first_name=message.text)
    await state.set_state(UserState.step_last_name)
    await message.answer("Введіть прізвище:", reply_markup=back_keyboard)


@auth_router.message(UserState.step_last_name)
async def ask_phone(message: Message, state: FSMContext):
    """
    Collects last name or returns to first name step.
    """

    if message.text == "Назад":
        # Exist => update
        await state.update_data(going_back=True)
        await state.set_state(UserState.step_first_name)
        await message.answer("⬅️ Введіть ім’я ще раз:", reply_markup=back_keyboard)
        return

    # Set/update state and send message
    await state.update_data(last_name=message.text)
    await state.set_state(UserState.step_phone)
    await message.answer(
        "Введіть номер телефону (у форматі +380...) або натисніть кнопку:",
        reply_markup=send_phone_keyboard,
    )


@auth_router.message(UserState.step_phone)
async def ask_birth_date(message: Message, state: FSMContext):
    """
    Collects phone number or returns to last name step.
    """

    if message.text == "Назад":
        # Exist => update
        await state.update_data(going_back=True)
        await state.set_state(UserState.step_last_name)
        await message.answer("⬅️ Введіть прізвище ще раз:", reply_markup=back_keyboard)
        return

    phone = message.contact.phone_number if message.contact else message.text

    # Set/update state and send message
    await state.update_data(phone_number=phone)
    await state.set_state(UserState.step_birth_date)
    await message.answer("Введіть дату народження (ДД.ММ.РРРР):", reply_markup=back_keyboard)


@auth_router.message(UserState.step_birth_date)
async def finish_registration(message: Message, state: FSMContext):
    """
    Completes registration or returns to phone input step.
    """

    if message.text == "Назад":
        # Exist => update
        await state.update_data(going_back=True)
        await state.set_state(UserState.step_phone)
        await message.answer(
            "⬅️ Введіть номер телефону ще раз:", reply_markup=send_phone_keyboard
        )
        return

    try:
        # Defined birthdate
        birth_date = datetime.strptime(message.text, "%d.%m.%Y").date()

    except ValueError:
        # Send error message
        await message.answer("❗️ Невірний формат. Спробуйте ще раз: ДД.ММ.РРРР", reply_markup=back_keyboard)
        return

    await state.update_data(date_of_birth=birth_date)

    # Defined user data
    data = await state.get_data()

    async for session in get_session():
        # Add realtor to DB
        realtor = Realtor(
            telegram_id=message.from_user.id,
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone_number=data["phone_number"],
            date_of_birth=data["date_of_birth"],
        )
        session.add(realtor)
        await session.commit()

    # Send success message
    await message.answer(
        "🎉 Реєстрацію завершено. Тепер ви можете додавати оголошення.",
        reply_markup=add_listing_keyboard,
    )
    await state.clear()
