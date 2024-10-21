from aiogram.fsm.state import State, StatesGroup

class SetConfigsToBot(StatesGroup):
    set_password = State()
    set_name = State()