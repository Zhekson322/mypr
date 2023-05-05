from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.callback_data import CallbackData #импортируем библиотеку для коллбеков




cb=CallbackData('ikb','action')#
dinam=CallbackData('markup','action') #шаблон создания динамической клавиатуры для услуг
dinamit=CallbackData('markup','action') #шаблон создания динамической клавиатуры подразделов услуг
myzapis=CallbackData('markup','action') #шаблон создания динамической клавиатуры для просмотра записей
myzapis_edit=CallbackData('markup','action') #шаблон создания динамической клавиатуры перезаписывания

def myzapis_ikb(data):#клавиатура для записанных услуг пользователя с кнопками изменить номер и тп
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    for i in data: # цикл для создания кнопок
        markup.add(InlineKeyboardButton(f'{i[3]}: {i[1]} {i[2]}', callback_data=dinam.new(i[0]))) #Создаём кнопки, i[1] - название, i[2] - каллбек дата
    markup.add(InlineKeyboardButton('📞Изменить номер телефона📞', callback_data=dinam.new('editphone')))
    markup.add(InlineKeyboardButton('Назад🏃', callback_data=dinam.new('nazad')))
    return markup #возвращаем клавиатуру

def myzapis_ikb_edit():  #кнопка для редактирования времени
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('📅Перезапись на другой день📅', callback_data=myzapis_edit.new('edit_time')))
    markup.add(InlineKeyboardButton('🔥Удалить время🔥', callback_data=myzapis_edit.new('delete_time')))
    markup.add(InlineKeyboardButton('Назад🏃', callback_data=myzapis_edit.new('nazad')))
    return markup

def menu_ikb() -> ReplyKeyboardMarkup:
    kb =ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/start - Перезапустить бота!'))
    return kb

def genmarkup(data): # передаём в функцию data, кортеж полученный из sql,клавиатура для выбора услуги
    markup = InlineKeyboardMarkup(row_width=2) # создаём клавиатуру
    for i in data: # цикл для создания кнопок
        markup.insert(InlineKeyboardButton(i[1], callback_data=dinam.new(i[1]))) #Создаём кнопки, i[1] - название, i[2] - каллбек дата
    markup.add(InlineKeyboardButton('Назад🏃', callback_data=dinam.new('nazad')))
    return markup #возвращаем клавиатуру

def get_time_zapis(data): # динамическая клавиатура для времени
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    for i in data: # цикл для создания кнопок
        markup.insert(InlineKeyboardButton(i[0], callback_data=cb.new(i[0]))) #Создаём кнопки, i[1] - название, i[2] - каллбек дата
    markup.add(InlineKeyboardButton('Назад🏃', callback_data=cb.new('nazadcalendar')))
    markup.add(InlineKeyboardButton('Главное меню🏃', callback_data=cb.new('nazad')))
    return markup #возвращаем клавиатуру

def all_uslugi(data): # передаём в функцию data, кортеж полученный из sql,клавиатура для выбора услуги
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    for i in data: # цикл для создания кнопок
        markup.add(InlineKeyboardButton(f'{i[2]}: {i[3]} руб', callback_data=dinamit.new(i[2]))) #Создаём кнопки, i[1] - название, i[2] - каллбек дата
    markup.add(InlineKeyboardButton('Назад🏃', callback_data=dinamit.new('nazad')))
    return markup #возвращаем клавиатуру


#динамическая клавиатура услуг


