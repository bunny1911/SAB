from aiogram.types import KeyboardButton


# All auth single buttons
register_button = KeyboardButton(text="📝 Зареєструватися")
login_button = KeyboardButton(text="🔐 Увійти")
add_listing_button = KeyboardButton(text="➕ Додати оголошення")
send_phone_button = KeyboardButton(text="📱 Надіслати мій номер", request_contact=True)
