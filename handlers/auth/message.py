from datetime import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from conf import REALTOR_PASSWORD
from db.base import get_session
from db.models.realtor import Realtor
from handlers.auth.buttom import main_kb, contact_kb, register_buttons
from handlers.auth.command import auth_router
from handlers.auth.schema import Register


@auth_router.callback_query(F.data == "register")
async def handle_register_click(
        callback: CallbackQuery,
        state: FSMContext
):
    # Set default value
    realtor = None

    async for session in get_session():
        realtor_query = await session.execute(
            select(Realtor).where(Realtor.telegram_id == callback.from_user.id)
        )
        realtor = realtor_query.scalar_one_or_none()

    if realtor:
        await callback.answer("Ви вже зареєстровані!", show_alert=True)
        return

    await callback.message.answer("Надішліть пароль для реєстрації:")
    await state.set_state(Register.ask_password)


@auth_router.message(Register.ask_password)
async def check_password(
        message: Message,
        state: FSMContext
):
    if message.text != REALTOR_PASSWORD:
        await message.answer("❌ Невірний пароль. Спробуйте ще раз:")
        return

    await message.answer("✅ Пароль підтверджено. Введіть ваше імʼя:")
    await state.set_state(Register.ask_first_name)


@auth_router.message(Register.ask_first_name)
async def ask_last_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Введіть ваше прізвище:")
    await state.set_state(Register.ask_last_name)


@auth_router.message(Register.ask_last_name)
async def ask_phone(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)

    await message.answer(
        "Введіть номер телефону (у форматі +380...) або натисніть кнопку:",
        reply_markup=contact_kb
    )
    await state.set_state(Register.ask_phone)


@auth_router.message(Register.ask_phone)
async def ask_birth_date(message: Message, state: FSMContext):
    phone = (
        message.contact.phone_number
        if message.contact
        else message.text
    )

    await state.update_data(phone_number=phone)
    await message.answer("Введіть дату народження (ДД.ММ.РРРР):")
    await state.set_state(Register.ask_birth_date)


@auth_router.message(Register.ask_birth_date)
async def finish_registration(message: Message, state: FSMContext):
    try:
        birth_date = datetime.strptime(message.text, "%d.%m.%Y").date()
    except ValueError:
        await message.answer("❗️ Невірний формат. Спробуйте ще раз: ДД.ММ.РРРР")
        return

    await state.update_data(date_of_birth=birth_date)
    data = await state.get_data()

    async for session in get_session():
        realtor = Realtor(
            telegram_id=message.from_user.id,
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone_number=data["phone_number"],
            date_of_birth=data["date_of_birth"],
        )
        session.add(realtor)
        await session.commit()

    await message.answer(
        "🎉 Реєстрацію завершено. Тепер ви можете додавати оголошення.",
        reply_markup=main_kb,
    )
    await state.clear()


@auth_router.callback_query(F.data == "login")
async def handle_login(callback: CallbackQuery, state: FSMContext):
    # Set default value
    realtor = None
    async for session in get_session():
        realtor_query = await session.execute(
            select(Realtor).where(Realtor.telegram_id == callback.from_user.id)
        )
        realtor = realtor_query.scalar_one_or_none()

    if not realtor:
        await callback.message.answer(
            "❗️ Вас ще не зареєстровано. Спочатку пройдіть реєстрацію.",
            reply_markup=register_buttons,
        )
        return

    await callback.message.answer("✅ Ви увійшли успішно.", reply_markup=main_kb)
    await state.clear()
