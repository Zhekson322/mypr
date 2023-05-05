from aiogram import types,Dispatcher
from bdbaza import sqlite as k
from user.users_kboard import *
from cgf.config import bot, UserState,FSMContext,dp,UserSpisok
from cgf.otherKB import menu,start_ikb #главное меню центральное
from user.zapis_handlers import btn_zapis,on_start




async def see_spisok(callback:types.CallbackQuery):
    kek=callback.message.chat.id
    result = await k.get_zapis(kek) #получаю записи пользователя
    print(result)
    if result==[]:
        await callback.answer("🤷‍♀️🤷‍♀️🤷‍♀ Вы еще не записаны 🤷‍♀️🤷‍♀️🤷‍♀️", show_alert=True)
    else:
        await callback.message.delete()
        Text= f'Номер телефона:<b> {result[0][6]} </b> \n' \
              f'Ваши записи:'
        await callback.message.answer(Text,parse_mode=types.ParseMode.HTML,reply_markup=myzapis_ikb(result))
        await UserSpisok.vibor.set()

async def take_callback_spisok_handler(callback:types.CallbackQuery,callback_data: dict,state: FSMContext):
    markup = InlineKeyboardMarkup().add(types.InlineKeyboardButton('Главное меню', callback_data='nazad'))
    await callback.message.delete()
    if callback_data['action']=='nazad':
        print('нажато назад')
        await state.finish()
        await on_start(callback.message)
    elif callback_data['action']=='editphone':
        print('смена номера телефона')
        await callback.message.answer('Укажите новый номер телефона:',reply_markup=markup)
        await UserSpisok.phone.set()
    else:
        #await callback.message.delete()
        print(callback_data['action'])
        await state.update_data(date_id=callback_data['action']) #сохраняю ид записи на услугу юзером(дата ид) для дальнейшего удаления
        result=await k.get_one_zapis(callback_data['action'])
        print(result)
        print(result[2])
        Text=f'Вы выбрали запись:\n' \
             f'{result[3]}: {result[1]} Время: {result[2]}\n' \
             f'<b>При нажатии на кнопку ваша запись будет удалена</b>'

        await callback.message.answer(Text,parse_mode=types.ParseMode.HTML,reply_markup=myzapis_ikb_edit())
        await UserSpisok.next()

async def perezapis_spisok_handler(callback:types.CallbackQuery,callback_data: dict,state: FSMContext):
    if callback_data['action']=='edit_time':
        result=await state.get_data() #получаю из состояний ид записи на услугу юзером
        await k.delet_zapis(result['date_id']) #вызываю запрос на обновление данных (очистке поля от юзера)
        print('Выполнено удаление юзера из записи')
        await callback.answer("Время удалено,вы можете перезаписаться:", show_alert=True)
        await state.finish()
        await btn_zapis(callback)
    elif callback_data['action']=='delete_time':
        result=await state.get_data() #получаю из состояний ид записи на услугу юзером
        await k.delet_zapis(result['date_id']) #вызываю запрос на обновление данных (очистке поля от юзера)
        print('Выполнено удаление юзера из записи')
        await callback.answer("🤷‍♂️Время удалено🤷‍♂️", show_alert=True)
        await state.finish()
        await on_start(callback.message)
    else:
        await state.finish()
        await see_spisok(callback)

async def edit_phone_number(message:types.Message,state: FSMContext):
    await bot.delete_message(message.chat.id,message.message_id-1) #удаляет "введите номер телефона"
    await k.update_phone(message.text,message.chat.id) #выполняется запрос
    print('Выполнено')
    await state.finish()
    await on_start(message)


def register_spisok_handlers(dp:Dispatcher) -> None:
    dp.register_callback_query_handler(see_spisok,text='push4') #выбор из услуг
    dp.register_callback_query_handler(take_callback_spisok_handler,myzapis.filter(),state=UserSpisok.vibor)
    dp.register_callback_query_handler(perezapis_spisok_handler,myzapis_edit.filter(),state=UserSpisok.edit)
    dp.register_message_handler(edit_phone_number,state=UserSpisok.phone)