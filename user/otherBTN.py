from aiogram import types,Dispatcher
from bdbaza import sqlite as k
from user.users_kboard import *
from user.zapis_handlers import on_start
from cgf.config import bot,dp, UserState,FSMContext #импорт из конфика бот и классы
from aiogram_calendar_rus import *
from datetime import datetime
from cgf.otherKB import start_ikb,menu #главное меню центральное



async def send_loc(callback:types.CallbackQuery):
    markup = InlineKeyboardMarkup().add(types.InlineKeyboardButton('Главное меню', callback_data='nazad'))
    markup.add(types.InlineKeyboardButton('Связаться с администратором',url='https://t.me/zheksod'))
    result=await k.get_opisanie()
    try:
        await callback.message.delete()
    except:
        print('Не удалось удалить')
    await callback.message.answer(result, parse_mode=types.ParseMode.HTML,disable_web_page_preview=True,reply_markup=markup)

async def nazad(callback:types.CallbackQuery):
    await on_start(callback.message)

def register_othter_handler(dp:Dispatcher) -> None:
    dp.register_callback_query_handler(send_loc,text='push3') #выбор из услуг
    dp.register_callback_query_handler(nazad,text='nazad')
