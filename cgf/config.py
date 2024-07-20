from aiogram import Bot, Dispatcher,executor
#from dotenv import load_dotenv
import os #взаимодействие с файловой системой
from aiogram.contrib.fsm_storage.memory import MemoryStorage #инициализировали память
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

TOKEN_API=''
admin_id='2104414456'
admin_id2='2104414456'

TOKEN_API=''
storage = MemoryStorage()  # память для

#load_dotenv('.env')
token = TOKEN_API
admin_key=admin_id
admin_key2=admin_id2
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())  # создаем объект диспетчер для работы с ботом и класс состояний

class UserState(StatesGroup):
    start=State()
    vibor =State() #выбор услуг
    final_vibor=State()
    zapis = State() #выбор даты
    zapisFinal = State() #выбор времени окошка
    set_name=State()
    phone = State() #финальный

class UserSpisok(StatesGroup):
    start=State()
    vibor=State()
    edit=State()
    phone=State()
    name=State()

class Adminka(StatesGroup):
    proverka=State() #состояние проверки рассылки текста
    send=State() #отправка текста
    take_excel=State() #состояние загрузки дат и времени
    take_excel_uslugi=State() #состояние загрузки разделов и услуг
    final_excel=State() #состояние записи под ключ

class Admin_Control(StatesGroup):
    take_zapis=State()
    delet_zapis=State()
    edit_klient=State()
    final_klient=State()
    edit_usluga=State()
    delet_usluga=State()
    price_usluga=State()

class Admin_Editor(StatesGroup):
    start=State()
    edit=State()





