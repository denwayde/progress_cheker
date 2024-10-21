from dotenv import load_dotenv
import os

load_dotenv()  # Загрузка переменных из файла .env
password = os.getenv('PASSWORD')


async def correct_password_proccess(message, state, bot, text, new_state):
    if message.text == password:
        await state.update_data(name = message.text)
        await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1))
        #await message.delete()
        #await message.answer_photo('http://www.gdk-ufa.ru/i/scheme.jpg')
        #await message.answer(text, reply_markup = get_places())
        await message.answer(text)
        await state.set_state(new_state)
    else:
        await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1))
        await message.answer('Вы ввели неверный пароль. Если Вы уверенны в правильности пароля попробуйте обратиться к администратору.')
        await state.clear()
