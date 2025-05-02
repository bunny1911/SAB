from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

register_keyboard = InlineKeyboardButton(text="📝 Зареєструватися", callback_data="register")
login_keyboard = InlineKeyboardButton(text="🔐 Увійти", callback_data="login")
auth_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            register_keyboard,
            login_keyboard,
        ]
    ]
)

register_buttons = InlineKeyboardMarkup(inline_keyboard=[[register_keyboard]])


main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="➕ Додати оголошення")]], resize_keyboard=True
)

contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Надіслати мій номер", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
