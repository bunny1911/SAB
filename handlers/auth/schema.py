from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    ask_password = State()
    ask_first_name = State()
    ask_last_name = State()
    ask_phone = State()
    ask_birth_date = State()
