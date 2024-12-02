from aiogram.fsm.state import State, StatesGroup

class SetConfigsToBot(StatesGroup):
    set_password = State()
    set_name = State()
    set_notification = State()
    set_user_names = State()
    edit_user_names = State()
    set_new_username = State()
    set_points_names = State()
    set_points_score = State()
    set_points_min = State()
    set_new_pointname = State()
    set_checkpoint = State()
    set_notification1 = State()
    set_notification2 = State()
    set_notification_final = State()
