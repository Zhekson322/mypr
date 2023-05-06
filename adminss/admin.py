from aiogram.utils.callback_data import CallbackData
from cgf.config import *
from bdbaza import sqlite as k
from aiogram import types
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup,KeyboardButton
from bdbaza import sqlite as k




def start_ikb(): #кнопки стартового меню админки
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('Показать все доступные записи'))
    markup.add(KeyboardButton('Показать всех записанных клиентов'))
    markup.add(KeyboardButton('/admin Перезапустить администратора'))
    return markup

dinam=CallbackData('markup','action') #шаблон создания динамической клавиатуры для услуг
mem=CallbackData('markup','action')
kewo=CallbackData('markup','action')
klient=CallbackData('markup','action')
kaw=CallbackData('markup','action')





def genmarkup(data): # передаём в функцию data, кортеж полученный из sql,клавиатура для выбора услуги
    markup = InlineKeyboardMarkup(row_width=2) # создаём клавиатуру
    for i in data: # цикл для создания кнопок
        if i[2]!='': #если есть юзер ид, значит запись не пустая
            markup.insert(InlineKeyboardButton(f'{i[1]} \n'
                                               f'🔥🔥🔥Запись🔥🔥🔥', callback_data=dinam.new(i[0])))  # Создаём кнопки, i[1] - название, i[2] - каллбек дата
        else:
            markup.insert(InlineKeyboardButton(i[1], callback_data=dinam.new(i[0]))) #Создаём кнопки, i[1] - название, i[2] - каллбек дата
    return markup #возвращаем клавиатуру


def get_user(data,ur): # передаём в функцию data, кортеж полученный из sql,клавиатура для вывода всех пользователей
    markup = InlineKeyboardMarkup(row_width=1) # создаём клавиатуру
    for i in data: # цикл для создания кнопок
        markup.insert(InlineKeyboardButton(f'{i[1]} {i[3]}. Время: {i[2]}', callback_data=klient.new(i[0]))) #Создаём кнопки, i[1] - название, i[2] - каллбек дата
    markup.add(InlineKeyboardButton('Написать пользователю🏃',url=ur))
    return markup #возвращаем клавиатуру

def danet():
    markup = InlineKeyboardMarkup(row_width=2)  # создаём клавиатуру
    markup.add(InlineKeyboardButton('Удалить время',callback_data=kewo.new('delet_time')))
    return markup


def inl_ikb():
    markup = InlineKeyboardMarkup(row_width=4)  # создаём клавиатуру
    markup.add(InlineKeyboardButton('Удалить время',callback_data=mem.new('delet_time')))
    markup.add(InlineKeyboardButton('Удалить запись(если есть)',callback_data=mem.new('delet_zapis')))
    markup.add(InlineKeyboardButton('Удалить всю дату со всем временем', callback_data=mem.new('delet_date')))
    return markup




##########################клавиатуры вверху###################################


#стартовая кнопка "Ручное управление"
async def rych_start(message: types.Message): #запись под ключ всего файла из екселя сразу
    if admin_key== str(message.chat.id) or admin_key2== str(message.chat.id):
        await message.answer('Нажмите кнопку:',reply_markup=start_ikb())
#Вывод всех доступных дат с колбеками
async def show_zapisi(message:types.Message,state:FSMContext):
    kek = await k.take_show_zapisi() #выбор уникальных дат из файла таблицы
    for i in kek: #i это мы берем дату из кека
        result=await k.take_show_time(i[0])
        await message.answer(f'Дата: {i[0]}',reply_markup=genmarkup(result)) #получаем инлайн кнопки с коллбеком из дате ид
    await Admin_Control.take_zapis.set() #переход в редактор дат

#нажатие на выбранное время по датам
async def take_zapis(callback:types.CallbackQuery,callback_data: dict,state:FSMContext):
    id = callback_data['action']
    await state.update_data(id_date=callback_data['action']) #сохраняем ид выбранной даты
    result =await k.get_one_zapis(id)
    await state.update_data(day_date=result[1]) #сохраняю день даты
    await state.update_data(date_time=result[2])#сохраняю время даты
    await state.update_data(user_id='')  # сохраняю время даты
    result2 = await state.get_data()
    if result[4]!='':
        await state.update_data(user_id=result[4])  # сохраняю время даты
        await callback.message.answer(f'Вы выбрали {result[1]}. Время: {result[2]}. Имеется запись "{result[3]}"\n'
                                      f'При продолжении запись будет стерта и придет уведомление клиенту \n'
                                      f'Введите /admin для выхода в меню администратора',reply_markup=inl_ikb())
    else:
        await callback.message.answer(f'Вы выбрали {result[1]}. Время: {result[2]}\n'
                                      f'Введите /admin для выхода в меню администратора',reply_markup=inl_ikb())
    await Admin_Control.next()

async def edit_zapis(callback:types.CallbackQuery,callback_data: dict,state:FSMContext):
    result2 = await state.get_data()  # получаем значения состояния машины из памяти
    #кнопка удаления времени
    if callback_data['action']=='delet_time':
        result2 = await state.get_data()
        if result2['user_id']!='':
            await bot.send_message(result2['user_id'],f'Ваша запись на {result2["day_date"]}, Время: {result2["date_time"]} \n'
                                                     f'Была отменена администратором')
            await callback.message.answer('Уведомление клиенту отправлено',reply_markup=start_ikb())
        else:
            await callback.message.answer('Успешно удалено',reply_markup=start_ikb())
        await k.delet_po_time(result2['id_date']) #удалить время по ид дата
    #кнопка удаления только записи
    elif callback_data['action']=='delet_zapis':
            if result2['user_id']!='':
                await k.delet_zapis(result2['id_date'])
                await bot.send_message(result2['user_id'],
                                       f'Ваша запись на {result2["day_date"]}, Время: {result2["date_time"]} \n'
                                       f'Была отменена администратором')
                await callback.message.answer('Уведомление клиенту отправлено', reply_markup=start_ikb())
            else:
                await callback.message.answer('На данный день нет записи',reply_markup=start_ikb())
    else:
        result3=await k.count_daty(result2['day_date'])
        if result3>0:
            await callback.message.answer('На эту дату имеются записи, сначала необходимо удалить их в ручную')
        else:
            await k.delet_daty(result2['day_date'])
            await callback.message.answer('День был полностью удален')

async def show_klienti(message:types.Message,state:FSMContext):
    Text=''
    nazv=''

    result=await k.take_zapisi_people()
    for i in result: #i это мы получили ид всех у кого есть записи
        Text=''
        if i[0]!='': #если ид не равен пустоте
            print(i)


            Text+=f'Имя: {i[1]} Телефон: {i[2]}\n' \
                  f'Записи:\n'
            l=await k.get_zapis(i[0]) #получаем записи по ид
            try:
                usern=await k.take_username(i[0]) #получаю юзернейм по иду
                ur=f'https://t.me/{usern}'
                await message.answer(Text, reply_markup=get_user(l, ur))
            except:

                print('id ne naiden')

    await message.answer('Нажмите на время для удаления пользователя')
    await Admin_Control.edit_klient.set()

async def show_edit_klienti(callback:types.CallbackQuery,callback_data: dict,state:FSMContext):
        result23 = await state.get_data()
        print(callback_data['action'])
        if callback_data['action']=='write_user':
            print(result23['user_id'])

        else:
            await state.update_data(date_id=callback_data['action'])
            l=await k.get_one_zapis(callback_data['action'])
            print(l)
            await state.update_data(user_id=l[4])
            await state.update_data(l1=l[1])
            await state.update_data(l2=l[2])
            await state.update_data(l3=l[3])
            await callback.message.answer(f'Вы собираетесь удалить запись пользователя:\n'
                                 f'{l[1]} {l[3]}. Время: {l[2]}',reply_markup=danet())
            await Admin_Control.next()


async def da_or_net(callback:types.CallbackQuery,callback_data: dict,state:FSMContext):
    print('Доходит сюда')
    if callback_data['action']=='delet_time':
        result = await state.get_data()
        await k.delet_zapis(result['date_id'])
        await bot.send_message(result['user_id'],f'Ваша запись:\n'
                                                 f' {result["l1"]} {result["l3"]}.Время: {result["l2"]}\n'
                                                 f'Была удалена администратором.')
        await callback.message.answer('Выполнено удаление, клиент был уведомлен.\n'
                                      'Обновите записи',reply_markup=start_ikb())
        await state.finish()




def register_admin_noexcel_handler(dp: Dispatcher) -> None:  # функция регистрации в дальнейшем передадим ее в мейн, и здесь
    dp.register_message_handler(rych_start,text='Ручное управление')
    dp.register_message_handler(show_zapisi,text='Показать все доступные записи',state='*')
    dp.register_callback_query_handler(take_zapis,dinam.filter(),state=Admin_Control.take_zapis)
    dp.register_callback_query_handler(edit_zapis,mem.filter(),state=Admin_Control.delet_zapis)
    dp.register_message_handler(show_klienti,text='Показать всех записанных клиентов',state='*')
    dp.register_callback_query_handler(show_edit_klienti,klient.filter(),state=Admin_Control.edit_klient)
    dp.register_callback_query_handler(da_or_net,kewo.filter(),state=Admin_Control.final_klient)
