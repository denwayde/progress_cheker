from dotenv import load_dotenv
import os
from btns.admin_options import admin_btns
from btns.user_options import user_btns
load_dotenv()  # Загрузка переменных из файла .env
password = os.getenv('PASSWORD')
admin_id = os.getenv('TELEGRAM_ID')

async def correct_password_proccess(message, state, bot, text, new_state):
    if message.text == password:
        if message.chat.id == admin_id:
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

async def if_admin(message):
    await message.answer('Добро пожаловать, администратор. Вам доступны следующие опции: Добавление или удаление имен пользователя, пунктов прогресса, минимумов прогресса, времени оповещения Вас, установление времени до которого должны оповестить Вас.\nЕсли у Вас возникнут вопросы, обращайтесь к https://t.me/Dinis_Fizik', reply_markup = admin_btns())

async def if_user(message):
    await message.answer('Добро пожаловать. Выберите пожалуйста имя которое предоставил Вам администратор.\nЕсли у Вас возникнут вопросы, обращайтесь к https://t.me/Dinis_Fizik')