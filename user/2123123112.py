from aiogram import types,Dispatcher
from bdbaza import sqlite as k
from user.users_kboard import *
from cgf.config import bot,dp, UserState,FSMContext #импорт из конфика бот и классы
from aiogram_calendar_rus import *
from datetime import datetime
from cgf.otherKB import start_ikb,menu #главное меню центральное




async def on_start(message:types.Message): #здесь мы передали вторым аргументом для записи пользователя в память
    print('сработафцаацфало')
    await k.user_add(message.chat.id,message.chat.first_name)
    await message.delete()
    await bot.send_photo(message.chat.id,photo='https://img-fotki.yandex.ru/get/3113/160997575.3b/0_101586_d138de9e_orig',
                        caption=f'Приветствую!{message.chat.first_name}!\nЧтобы вы хотели?',reply_markup=start_ikb())




#выбор услуг
async def btn_zapis(callback:types.CallbackQuery):
       await callback.message.delete()
       count=await k.db_uslugi() #получил результат метода sql запроса выборка
       await callback.message.answer(f'Выберите,что вас интересует:',reply_markup=genmarkup(count))
       await UserState.vibor.set() #переход в состояние календапя
       #здесь добавить состояние переход



#получение даты из календаря
async def btn_vibor(callback:types.CallbackQuery,callback_data: dict,state: FSMContext): #state:FSMContext для сохранения данных
        if callback_data['action']=='nazad': #проверка на кнопку назад, если что вызываем метод указанный
            print(callback.message.text)
            await state.finish()
            await on_start(callback.message) #передаем сюда сообщение
        else:
            await callback.message.delete()
            await state.update_data(chat_id=callback.message.chat.id)
            await state.update_data(usluga=callback_data['action']) #сохраняем usluga в память состояния для дальнейшей записи
            #здесь добавим подпункты
            result=await state.get_data()
            result_uslug= await k.db_all_uslugi(result['usluga'])
            await callback.message.answer(f'Раздел:<b> {result["usluga"]} </b>, выберите услугу для записи:',parse_mode=types.ParseMode.HTML,reply_markup=all_uslugi(result_uslug))
            await UserState.next()
            #await callback.message.answer(f'Вы выбрали {callback_data["action"]}, укажите дату:',reply_markup=await SimpleCalendar().start_calendar())
            #await UserState.next() #переход в состояние выбора даты

#получение всех услуг из подпункта с ценой и т.п
async def btn_vibor_uslug(callback:types.CallbackQuery,callback_data: dict,state: FSMContext):
        print(callback_data['action'])
        result_uslugi=await k.price_all_uslgugi(callback_data['action']) #получение стоимости услуги по коллбеку
        print(result_uslugi[0][0])#вывод стоимости из кортежа
        await state.update_data(price_uslugi=result_uslugi[0][0])
        result = await state.get_data()
        await callback.message.answer(f'Вы выбрали <b> {result["usluga"]}</b>,\n'
                                      f'Стоимость:<b>{result["price_uslugi"]} РУБ</b> \n'
                                      f'Укажите дату:',parse_mode=types.ParseMode.HTML,reply_markup=await SimpleCalendar().start_calendar())
        await UserState.next() #переход в состояние выбора даты


# получение времени после даты
async def process_simple_calendar(callback_query:types.CallbackQuery, callback_data: dict,state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)

    markup = InlineKeyboardMarkup().add(types.InlineKeyboardButton('Главное меню', callback_data='nazad'))
    if selected:
        await callback_query.message.delete()
        if datetime.now().day<=int(date.strftime("%d")) or datetime.now().month<int(date.strftime("%m")) :
            #сравниваю день с выбранным днем или месяц с нынешним месяцом
            #чтобы нельзя было выбирать старые дни, а также по месяцам чтобы можно было в след месяца
            await state.update_data(time_date=date.strftime("%Y-%m-%d"))
            result=await state.get_data() #получаем в переменную данные из памяти состояний
            count1=await k.proverka_zapisi(result['time_date'],result['usluga'],result['chat_id'])
            if count1>=1: #если записей на дату и услугу больше одного от пользователя, то нельзя дальше
                await state.finish()
                await callback_query.message.answer(f"Вы уже записаны на {result['usluga']} в этот день.\n"
                                                    f"Перейдите в главное меню чтобы перезаписаться или отменить запись.",reply_markup=markup)

            else:
                count=await k.get_time_uslug(result['time_date'],result['usluga']) #sql запрос для получения времени по дату и услуги
                await callback_query.message.answer(
                f'Вы выбрали {result["usluga"]}.\nДата: {date.strftime("%d/%m/%Y")}. \nВыберите из доступного времени:',
                    reply_markup=get_time_zapis(count))
                await UserState.next()
        else:
            await callback_query.message.answer('Вы выбрали дату, которая уже прошла,выберите снова',reply_markup=await SimpleCalendar().start_calendar())
            await UserState.zapis.set()



#указ номера телефона
async def final_zapis(callback:types.CallbackQuery,callback_data: dict,state: FSMContext):
    markup = InlineKeyboardMarkup().add(types.InlineKeyboardButton('Отменить запись',callback_data='nazad'))
    result = await state.get_data()  # получаем значения состояния машины из памяти
    if callback_data['action']=='nazadcalendar':
        await callback.message.delete()
        await callback.message.answer(f'Вы выбрали {result["usluga"]}, укажите дату:',reply_markup=await SimpleCalendar().start_calendar())
        await UserState.zapis.set()
    elif callback_data['action'] == 'nazad':  # проверка на кнопку назад, если что вызываем метод указанный
        print(callback_data['action'])
        await state.finish()
        await on_start(callback.message)  # передаем сюда сообщение
    else:
        await callback.message.delete()
        await state.update_data(t_zapis=callback_data['action'])
       # result = await state.get_data()#получаем значения состояния машины из памяти
        await callback.message.answer(f'Вы выбрали запись на {result["usluga"]}.\n'
                                      f'Дата: {result["time_date"]} \n'
                                      f'Время: {result["t_zapis"]} \n'
                                      f'Чтобы записаться, УКАЖИТЕ ваш <b><u>номер телефона</u></b>:',parse_mode=types.ParseMode.HTML,reply_markup=markup)

        await UserState.next()


#ждет номера телефона
async def vvod_phone(message:types.Message,state: FSMContext):
        markup = InlineKeyboardMarkup().add(types.InlineKeyboardButton('Главное меню',callback_data='nazad'))
        await bot.delete_message(message.chat.id,message.message_id-1)
        await message.delete()
        await state.update_data(phone=message.text)
        await state.update_data(id_user=message.chat.id)
        await state.update_data(name_user=message.from_user.first_name)
        result = await state.get_data()#получаем значения состояния машины из памяти
        await k.update_phone(result['phone'],result['id_user'])
        await k.zapis_final(result['id_user'],result['name_user'],result['phone'],result['time_date'],result['t_zapis'],result['usluga'])
        await message.answer(f'Вы записались на <b>{result["usluga"]}</b>.\n'
                                      f'Дата: {result["time_date"]} \n'
                                      f'Время: {result["t_zapis"]} \n'
                                      f'Ваш номер:: {result["phone"]} \n'
                                      f'Отменить запись или изменить номер можно из главного меню',parse_mode=types.ParseMode.HTML,reply_markup=markup)
        await state.finish()


async def keksik(callback:types.CallbackQuery,state: FSMContext): #назад при вводе номера телефона9(для машины состояний)
    await state.finish()
    print('Пашет')
    await on_start(callback.message)


async def on_start_restart(message:types.Message,state: FSMContext): #здесь мы передали вторым аргументом для записи пользователя в память
    await state.finish()
    await k.user_add(message.chat.id,message.chat.first_name)
    await message.delete()
    await bot.send_photo(message.chat.id,photo='https://img-fotki.yandex.ru/get/3113/160997575.3b/0_101586_d138de9e_orig',
                        caption=f'Приветствую!{message.chat.first_name}!\nЧтобы вы хотели?',reply_markup=start_ikb())

def register_user_handlers(dp:Dispatcher) -> None: #функция регистрации в дальнейшем передадим ее в мейн, и здесь
    print('Прошел метод основного меню')
    dp.register_message_handler(on_start,commands=['start']) #старт
    dp.register_callback_query_handler(btn_zapis,text='push1') #выбор из услуг
    dp.register_callback_query_handler(btn_vibor,dinam.filter(),state=UserState.vibor) #выбор даты из календаря
    dp.register_callback_query_handler(btn_vibor_uslug,dinamit.filter(),state=UserState.final_vibor) #выбор даты из календаря
    dp.register_callback_query_handler(process_simple_calendar,simple_cal_callback.filter(),state=UserState.zapis)#выбор времени,проверка на перезапись
    dp.register_callback_query_handler(final_zapis,cb.filter(),state=UserState.zapisFinal) #указать номер телефона
    dp.register_callback_query_handler(keksik,text='nazad',state='*')
    dp.register_message_handler(vvod_phone,state=UserState.phone) #ждет указания номера телефона

    dp.register_message_handler(on_start_restart,commands=['start'],state='*') #чтобы в любой момент можно было рестарт сделать /start(выход из состояния)



