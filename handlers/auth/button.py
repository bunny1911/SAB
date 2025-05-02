from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from handlers.base.button import cancel_keyboard

# All single keyboards
register_keyboard = InlineKeyboardButton(
    text="📝 Зареєструватися", callback_data="register"
)
login_keyboard = InlineKeyboardButton(text="🔐 Увійти", callback_data="login")
add_listing_keyboard = KeyboardButton(text="➕ Додати оголошення")
send_phone_keyboard = KeyboardButton(text="📱 Надіслати мій номер", request_contact=True)


# All buttons
auth_buttons = InlineKeyboardMarkup(inline_keyboard=[[register_keyboard, login_keyboard]])
register_buttons = InlineKeyboardMarkup(inline_keyboard=[[register_keyboard]])
add_listing_buttons = ReplyKeyboardMarkup(
    keyboard=[[add_listing_keyboard, cancel_keyboard]],
    resize_keyboard=True,
)
send_phone_buttons = ReplyKeyboardMarkup(
    keyboard=[[send_phone_keyboard, cancel_keyboard]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
