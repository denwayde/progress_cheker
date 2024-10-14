from btns.forPlace import get_places

async def name_proccessor(message, state, bot, text, new_state):
    await state.update_data(name = message.text)
    await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1))
    #await message.delete()
    await message.answer_photo('http://www.gdk-ufa.ru/i/scheme.jpg')
    await message.answer(text, reply_markup = get_places())
    await state.set_state(new_state)

#SetConfigsToBot.set_place
#f"Приятно познакомиться, {message.text}. Выберите пожалуйста область зала"