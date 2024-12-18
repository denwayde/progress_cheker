async def start_func(message, state, text, new_state, bot):
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer(text)
    await state.set_state(new_state)
    #"Здравствуйте, Вас приветсвует бот, который поможет Вам забронировать место в зале. Давайте приступим.\nНапишите пожалуйста боту ФИО"
    #SetConfigsToBot.set_name
