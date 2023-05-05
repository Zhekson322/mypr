from aiogram.utils.callback_data import CallbackData
from cgf.config import *
from bdbaza import sqlite as k
from aiogram import types
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup,KeyboardButton
from bdbaza import sqlite as k


keksik="""
<b>Жирный шрифт</b>
<code>Текст для копирования</code>
<u>Подчеркнутый текст</u>
<s>Зачеркнутый текст</s>
<a href='vk.com'>Текст ссылки</a>
<i>Курсивный текст</i>"""

########################изменение главного меню####################
async def edit_location(message:types.Message):
    if admin_key== str(message.chat.id) or admin_key2== str(message.chat.id):
        await message.answer('Отправьте главное фото')

async def take_location(message:types.Message):
    if admin_key== str(message.chat.id) or admin_key2== str(message.chat.id):
        result=await k.get_location()
        await message.photo[-1].download(destination_file='cgf/test.jpg')
        await message.answer(f'Фото сохранено,отправьте стартовый текст по примеру:\n'
                             f'{keksik}')
        await message.answer(keksik,parse_mode=types.ParseMode.HTML,disable_web_page_preview=True)
        await message.answer('ВАШ СТАРЫЙ ТЕКСТ \n'
                             f'{result}')

async def final_menu(message:types.Message):
    if admin_key== str(message.chat.id) or admin_key2== str(message.chat.id):
        await k.give_location(message.text)
        await message.answer('Проверьте результат командой /start')
#########################изменение информации#############################

async def inf_btn(message:types.Message):
    if admin_key== str(message.chat.id) or admin_key2== str(message.chat.id):
        await message.answer('Отправьте сообщение, здесь вы можете указать адрес, ссылки на соц сети, номер телефона и тому подобное')
        await message.answer(f'Пример оформления текста:\n'
                             f'{keksik}')
        await message.answer(keksik,parse_mode=types.ParseMode.HTML,disable_web_page_preview=True)
        await message.answer('Отправьте ваш текст:')
        await Admin_Editor.start.set()

async def final_inf(message:types.Message,state:FSMContext):
    await state.finish()
    await k.infa(message.text)
    await message.answer('Проверьте результат можно через кнопку из главного меню /start')

def register_admin_editor_handler(dp: Dispatcher) -> None:  # функция регистрации в дальнейшем передадим ее в мейн, и здесь
    dp.register_message_handler(edit_location,text='Настройка стартового меню')
    dp.register_message_handler(take_location,content_types=['photo','rb'])
    dp.register_message_handler(inf_btn,text='Настройка кнопки "Информация"')
    dp.register_message_handler(final_menu,content_types=['text'])

    dp.register_message_handler(final_inf,content_types=['text'],state=Admin_Editor.start)