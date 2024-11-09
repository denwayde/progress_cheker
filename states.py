from aiogram.fsm.state import State, StatesGroup

class SetConfigsToBot(StatesGroup):
    set_password = State()
    set_name = State()
    set_user_names = State()
    edit_user_names = State()
    set_new_username = State()
    set_points_names = State()
    set_new_pointname = State()