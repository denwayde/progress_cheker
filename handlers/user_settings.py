from btns.users_edit_btns import get_users_settings
async def call_users_settings(call, bot):
    await call.message.answer(f"Выберите пожалуйста опцию", reply_markup = get_users_settings())
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()
    #await state.set_state(state_param)