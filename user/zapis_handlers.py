from aiogram import types,Dispatcher
from bdbaza import sqlite as k
from user.users_kboard import *
from cgf.config import bot,dp, UserState,FSMContext #импорт из конфика бот и классы
from aiogram_calendar_rus import *
from datetime import datetime
from cgf.otherKB import start_ikb,menu #главное меню центральное


name_user=''

async def on_start(message:types.Message): #здесь мы передали вторым аргументом для записи пользователя в память
    try:
        await k.delete_starie()
        print('Старые записи удалены')
        await message.delete()
    except:
        print('Старых записей нет')
    global name_user
    name_user=message.chat.first_name
    try:
        await k.user_add(message.chat.id,message.chat.first_name,message.from_user.username)
    except:
        await k.user_add(message.chat.id, message.chat.first_name,'Null')
    result = await k.get_location()
    file=open('cgf/test.jpg','rb')
    await bot.send_photo(message.chat.id,photo=file,
                        caption=result,parse_mode=types.ParseMode.HTML,reply_markup=start_ikb())




#выбор услуг
async def btn_zapis(callback:types.CallbackQuery):
    try:
       await callback.message.delete()
    except:
        print('Не получилось удалить код 31')
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
            print(result_uslug)
            if result_uslug==[]:
                await callback.message.answer(f'Раздел:<b> {result["usluga"]} </b> \n'
                                              f'\n'
                                              f'<b>На данный раздел не добавлены услуги для записи, обратитесь к администратору.</b>',
                                              parse_mode=types.ParseMode.HTML, reply_markup=all_uslugi(result_uslug))
            else:
                await callback.message.answer(f'Раздел:<b> {result["usluga"]} </b>, выберите услугу для записи:',parse_mode=types.ParseMode.HTML,reply_markup=all_uslugi(result_uslug))
            await UserState.next()


#получение всех услуг из подпункта с ценой и т.п
async def btn_vibor_uslug(callback:types.CallbackQuery,callback_data: dict,state: FSMContext):
        if callback_data['action']=='nazad': #проверка на кнопку назад, если что вызываем метод указанный
            print(callback.message.text)
            await state.finish()
            await btn_zapis(callback)
        else:
            await callback.message.delete()
            print(callback_data['action'])
            await state.update_data(
            usluga=callback_data['action'])  # сохраняем usluga в память состояния для дальнейшей записи
            result_uslugi=await k.price_all_uslgugi(callback_data['action']) #получение стоимости услуги по коллбеку
            #print(result_uslugi[0][0])#вывод стоимости из кортежа
            await state.update_data(price_uslugi=result_uslugi[0][0])
            result = await state.get_data()
            await callback.message.answer(f'Вы выбрали: <b> {result["usluga"]}</b>\n'
                                          f'Стоимость: <b>{result["price_uslugi"]} РУБ</b> \n'
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
                print(f'Каунт{count}')
                if count==[]:
                    await callback_query.message.answer(
                        f'Вы выбрали<b> {result["usluga"]}.</b>\nДата: <b>{date.strftime("%d/%m/%Y")}.</b> \n'
                        f'<b>НА ДАННУЮ ДАТУ НЕТ ДОСТУПНОГО ВРЕМЕНИ</b>:', parse_mode=types.ParseMode.HTML,
                        reply_markup=get_time_zapis(count))
                else:
                    await callback_query.message.answer(
                    f'Вы выбрали<b> {result["usluga"]}.</b>\nДата: <b>{date.strftime("%d/%m/%Y")}.</b> \n'
                    f'Выберите из доступного времени:',parse_mode=types.ParseMode.HTML,
                        reply_markup=get_time_zapis(count))
                await UserState.next()
        else:
            await callback_query.message.answer('Вы выбрали дату, которая уже прошла,выберите снова.',reply_markup=await SimpleCalendar().start_calendar())
            await UserState.zapis.set()



#указ номера телефона
async def final_zapis(callback:types.CallbackQuery,callback_data: dict,state: FSMContext):
    markup = InlineKeyboardMarkup().add(types.InlineKeyboardButton('Отменить запись',callback_data='nazad'))
    result = await state.get_data()
    #try:
     #   kek = await k.get_phone(result['chat_id'])
      #  await state.update_data(phone=kek)
       # if kek!='Null':
        #    markup.add(types.InlineKeyboardButton(kek,callback_data='phone')) #добавление инлайн кнопки с номером если ест
    #except:
    #    print('Номер телефона не найден')

    try:
        kek=await k.get_name(result['chat_id'])
        await state.update_data(name_user=kek)

        markup.add(
            types.InlineKeyboardButton(kek, callback_data='us_name'))  # добавление инлайн кнопки с номером если ест
    except:
         print('Не удалось')

    if callback_data['action']=='nazadcalendar':
        await state.finish()
        await btn_zapis(callback)
        #await callback.message.answer(f'Вы выбрали: <b> {result["usluga"]}</b>\n'
        #                              f'Стоимость: <b>{result["price_uslugi"]} РУБ</b> \n'
        #                              f'Укажите дату:',parse_mode=types.ParseMode.HTML,reply_markup=await SimpleCalendar().start_calendar())
    elif callback_data['action'] == 'nazad':  # проверка на кнопку назад, если что вызываем метод указанный
        await state.finish()
        await on_start(callback.message)  # передаем сюда сообщение
    else:
        await callback.message.delete()
        await state.update_data(t_zapis=callback_data['action'])
        result = await state.get_data()  # получаем значения состояния машины из памяти
       # result = await state.get_data()#получаем значения состояния машины из памяти
        await callback.message.answer(f'Вы выбрали <b>{result["usluga"]}</b>\n'
                                      f'Стоимость: <b>{result["price_uslugi"]} РУБ</b>\n'
                                      f'Дата:<b> {result["time_date"]}</b> \n'
                                      f'Время:<b> {result["t_zapis"]}</b> \n'
                                      f'Чтобы записаться, УКАЖИТЕ <b><u>как к вам обращаться</u></b>:',
                                      parse_mode=types.ParseMode.HTML, reply_markup=markup)
                                     # f'Чтобы записаться, УКАЖИТЕ ваш <b><u>номер телефона</u></b>:',parse_mode=types.ParseMode.HTML,reply_markup=markup)

        await UserState.next()

###########################################вввод сообщения
async def get_name(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup().add(types.InlineKeyboardButton('Отменить запись',callback_data='nazad'))
    result = await state.get_data()
    try:
        await state.update_data(name_user=message.text)
        kek = await k.get_phone(result['chat_id'])
        await state.update_data(phone=kek)
        if kek!='Null':
            markup.add(types.InlineKeyboardButton(kek,callback_data='phone')) #добавление инлайн кнопки с номером если ест
    except:
        print('Номер телефона не найден')


    #await state.update_data(name_user=message.text)
    try:
        await bot.delete_message(message.chat.id,message.message_id-1)
        await message.delete()
    except:
        print('Не удалось удалить22')
    await state.update_data(id_user=message.chat.id)
    result = await state.get_data()#получаем значения состояния машины из памяти
    await k.user_name(result['name_user'],result['id_user'])
    await message.answer(f'Вы указали имя: <b>{result["name_user"]}</b>\n'
                                  f'<b>Теперь укажите номер телефона для связи с вами:</b>',reply_markup=markup,parse_mode=types.ParseMode.HTML)
    await UserState.next()

#################################
async def get_name_c(callback:types.CallbackQuery,state: FSMContext): #колбек если у пользователя уже сохранен номер телефона
    markup = InlineKeyboardMarkup().add(types.InlineKeyboardButton('Главное меню', callback_data='nazad'))
    await callback.message.delete()

    await state.update_data(id_user=callback.message.chat.id)
    result = await state.get_data()  # получаем значения состояния машины из памяти
    try:
        kek = await k.get_phone(result['chat_id'])
        await state.update_data(phone=kek)
        if kek!='Null':
            markup.add(types.InlineKeyboardButton(kek,callback_data='phone')) #добавление инлайн кнопки с номером если ест
    except:
        print('Номер телефона не найден')

    await k.user_name(result['name_user'], result['id_user'])
    await callback.message.answer(f'Вы указали имя: <b>{result["name_user"]}</b>\n'
                         f'<b>Теперь укажите номер телефона для связи с вами:</b>', reply_markup=markup,
                         parse_mode=types.ParseMode.HTML)
    await UserState.next()

####################################

async def vvod_phone_c(callback:types.CallbackQuery,state: FSMContext): #колбек если у пользователя уже сохранен номер телефона
    markup = InlineKeyboardMarkup().add(types.InlineKeyboardButton('Главное меню', callback_data='nazad'))
    await callback.message.delete()
    await state.update_data(id_user=callback.message.chat.id)
    result = await state.get_data()  # получаем значения состояния машины из памяти
    print(result)
    await k.zapis_final2(result['id_user'],result['name_user'], result['phone'], result['time_date'], result['t_zapis'],result['usluga'])

    await callback.message.answer(f'Ваше имя:<b>{result["name_user"]}</b>\n'
                                  f'Ваша запись: <b>{result["usluga"]}</b>.\n'
                         f'Дата: <b>{result["time_date"]}</b> \n'
                         f'Время: <b>{result["t_zapis"]}</b> \n'
                         f'Ваш номер:<b> {result["phone"]}</b> \n'
                         f'Отменить запись или изменить номер можно из главного меню.', parse_mode=types.ParseMode.HTML,
                         reply_markup=markup)

    usern = await k.take_username(result['id_user'])  # получаю юзернейм по иду
    ur = f'https://t.me/{usern}'
    markup1 = InlineKeyboardMarkup().add(types.InlineKeyboardButton('Написать клиенту', url=ur))

    await bot.send_message("2104414456", f'Появилась новая запись на <b>{result["usluga"]}</b>.\n'
                                         f'Дата: <b>{result["time_date"]}</b> \n'
                                         f'Время:<b> {result["t_zapis"]}</b> \n'
                                         f'Имя:{result["name_user"]}\n </b>'
                                         f'Номер:<b>{result["phone"]} \n</b>',parse_mode=types.ParseMode.HTML,
                           reply_markup=markup1)

    await state.finish()



#ждет номера телефона
async def vvod_phone(message:types.Message,state: FSMContext):
        markup = InlineKeyboardMarkup().add(types.InlineKeyboardButton('Главное меню',callback_data='nazad'))
        try:
            await bot.delete_message(message.chat.id,message.message_id-1)
            await message.delete()
        except:
            print('Не получилось удалить сообщение')

        await state.update_data(phone=message.text)
        await state.update_data(id_user=message.chat.id)
        await state.update_data(name_user=message.from_user.first_name)
        result = await state.get_data()#получаем значения состояния машины из памяти
        await k.update_phone(result['phone'],result['id_user'])
        await k.zapis_final(result['id_user'],result['name_user'],result['phone'],result['time_date'],result['t_zapis'],result['usluga'])
        await message.answer(f'Вы записались на <b>{result["usluga"]}</b>.\n'
                                      f'Ваше имя: {result["name_user"]}\n'
                                      f'Дата: {result["time_date"]} \n'
                                      f'Время: {result["t_zapis"]} \n'
                                      f'Ваш номер:: {result["phone"]} \n'
                                      f'Отменить запись или изменить номер можно из главного меню',parse_mode=types.ParseMode.HTML,reply_markup=markup)
        usern = await k.take_username(result['id_user'])  # получаю юзернейм по иду
        ur = f'https://t.me/{usern}'
        markup1 = InlineKeyboardMarkup().add(types.InlineKeyboardButton('Написать клиенту', url=ur))

        await bot.send_message("2104414456", f'Появилась новая запись на <b>{result["usluga"]}</b>.\n'
                                             f'Дата: {result["time_date"]} \n'
                                             f'Время: {result["t_zapis"]} \n'
                                             f'Имя:{result["name_user"]}\n'
                                             f'Номер: {result["phone"]} \n', parse_mode=types.ParseMode.HTML,
                               reply_markup=markup1)

        await state.finish()


async def keksik(callback:types.CallbackQuery,state: FSMContext): #назад при вводе номера телефона9(для машины состояний)
    await state.finish()
    await on_start(callback.message)


async def on_start_restart(message:types.Message,state: FSMContext): #здесь мы передали вторым аргументом для записи пользователя в память
    try:
        await state.finish()
    except:
        print('Состояние отсутствует')
    try:
        await k.delete_starie()
        print('Старые записи удалены')
        await message.delete()
    except:
        print('Старых записей нет')
    global name_user
    name_user=message.chat.first_name
    try:
        await k.user_add(message.chat.id,message.chat.first_name,message.from_user.username)
    except:
        await k.user_add(message.chat.id, message.chat.first_name,'Null')
    result = await k.get_location()
    file=open('cgf/test.jpg','rb')
    await bot.send_photo(message.chat.id,photo=file,
                        caption=result,parse_mode=types.ParseMode.HTML,reply_markup=start_ikb())

def register_user_handlers(dp:Dispatcher) -> None: #функция регистрации в дальнейшем передадим ее в мейн, и здесь
    dp.register_message_handler(on_start,commands=['start']) #старт
    dp.register_callback_query_handler(btn_zapis,text='push1') #выбор из услуг
    dp.register_callback_query_handler(btn_vibor,dinam.filter(),state=UserState.vibor) #выбор даты из календаря
    dp.register_callback_query_handler(btn_vibor_uslug,dinamit.filter(),state=UserState.final_vibor) #выбор даты из календаря
    dp.register_callback_query_handler(process_simple_calendar,simple_cal_callback.filter(),state=UserState.zapis)#выбор времени,проверка на перезапись
    dp.register_callback_query_handler(final_zapis,cb.filter(),state=UserState.zapisFinal) #указать номер телефона
    dp.register_callback_query_handler(keksik,text='nazad',state='*')
    dp.register_message_handler(get_name,state=UserState.set_name)
    dp.register_callback_query_handler(get_name_c,text='us_name',state=UserState.set_name)
    dp.register_callback_query_handler(vvod_phone_c,text='phone',state=UserState.phone)
    dp.register_message_handler(vvod_phone,state=UserState.phone) #ждет указания номера телефона

    dp.register_message_handler(on_start_restart,commands=['start'],state='*') #чтобы в любой момент можно было рестарт сделать /start(выход из состояния)



