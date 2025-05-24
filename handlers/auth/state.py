from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    """
    FSM for step-by-step user registration.
    """

    step_password: State = State()
    step_first_name: State = State()
    step_last_name: State = State()
    step_phone: State = State()
    step_birth_date: State = State()
