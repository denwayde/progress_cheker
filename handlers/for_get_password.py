from dotenv import load_dotenv
import os
load_dotenv()  # Загрузка переменных из файла .env
password = os.getenv('PASSWORD')
admin_id = os.getenv('ADMIN_ID')
#from btns.admin_options import admin_btns
from db_func import delete_or_insert_data
from btns.admin_replybtn import admin_replybtns
from btns.user_options import user_btns
from states import SetConfigsToBot


async def correct_password_proccess(message, state, bot):
    if message.text == password:
        # print(type(message.chat.id))
        # print(type(admin_id))
        if message.chat.id == int(admin_id):
            await if_admin(message, state)
            await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1))
        else:
            await if_user(message, bot, state, 'Добро пожаловать. Напишите пожалуйста никнейм, который предоставил Вам администратор.', SetConfigsToBot.set_name)
        
    else:
        await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1))
        await message.answer('Вы ввели неверный пароль. Попробуйте сделать это снова нажав на /start. Если Вы уверенны в правильности пароля, но это сообщение выходит снова попробуйте обратиться к администратору.')
        await state.clear()


async def if_admin(message, state):
    await state.clear()
    delete_or_insert_data("INSERT INTO admin (name, telega_id) VALUES (?, ?)", ('Admin', message.chat.id))
    await message.answer('Добро пожаловать, администратор. Вам доступны следующие опции: Добавление или удаление имен пользователя, пунктов прогресса, минимумов прогресса, времени оповещения Вас, установление времени до которого должны оповестить Вас.\n\nЕсли у Вас возникнут вопросы, обращайтесь к @Dinis_Fizik', reply_markup = admin_replybtns())
    

#from btns.users_for_edit import users_for_edit
async def if_user(message, bot, state, message_text, new_state):
    await message.answer(message_text)#, reply_markup=users_for_edit('userchosen_name_')
    await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1))
    await state.set_state(new_state)