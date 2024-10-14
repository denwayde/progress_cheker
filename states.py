from aiogram.fsm.state import State, StatesGroup

class SetConfigsToBot(StatesGroup):
    set_name = State()