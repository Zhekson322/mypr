from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.callback_data import CallbackData #импортируем библиотеку для коллбеков


#главное меню кнопки
menu=CallbackData('ikb','action') #шаблон главного меню при старте

def start_ikb() -> InlineKeyboardMarkup: #клавиатура главного меню
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Записаться:',callback_data='push1')],
        [InlineKeyboardButton('Информация:',callback_data='push3'),
         InlineKeyboardButton('Мои записи:', callback_data='push4')]
    ])
    return ikb