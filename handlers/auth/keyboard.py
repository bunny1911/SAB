from aiogram.types import ReplyKeyboardMarkup

from handlers.auth.button import *
from handlers.base.button import back_button, exit_button


# All keyboard
back_keyboard = ReplyKeyboardMarkup(
    keyboard=[[back_button, exit_button]],
    resize_keyboard=True,
    one_time_keyboard=True
)
auth_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [register_button, login_button],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
register_keyboard = ReplyKeyboardMarkup(
    keyboard=[[register_button]],
    resize_keyboard=True,
)
add_listing_keyboard = ReplyKeyboardMarkup(
    keyboard=[[add_listing_button, exit_button]],
    resize_keyboard=True,
)
send_phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[[send_phone_button, back_button, exit_button,]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
