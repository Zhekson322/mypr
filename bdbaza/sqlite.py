
import sqlite3 as sq
from datetime import datetime
import datetime


async def db_start():
    global  db,cur
    db=sq.connect('bdbaza/baza.db')
    cur=db.cursor()
    print('База подключена')
    all_uslug=cur.execute("SELECT COUNT(*) FROM uslugi").fetchone()[0]
    print('Выполнн')


    return  all_uslug



async def testsql():
    print('Импорт из sql')
    return

async def user_add(user_id,first_name,mess): #добавление пользователя в базу
        kek=cur.execute('SELECT COUNT(*) FROM user WHERE user_id=(?);',(user_id,)).fetchone()[0]
        if kek==0:
            cur.execute('INSERT INTO user VALUES (?,?,?,?,?);',(user_id,first_name,'Null',datetime.date.today(),mess))
            db.commit()
            print('Выполнено добавление юзера')
        else:
            print('Добавление пользователя не нужно')
        return kek


async def proverka_zapisi(date_u,name_u,user_id):
    kek=cur.execute('SELECT COUNT(*) FROM time_uslugi WHERE date_u=(?) and name_u=(?) and user_id=(?);',(date_u,name_u,user_id,)).fetchone()[0]
    return kek


async def get_phone(user_id):  # проверка есть ли у пользователя номер телефона
    #kek=cur.execute('SELECT COUNT(*) FROM user WHERE user_id=(?) and NOT phone_user="";',(user_id,)).fetchone()[0]
    kek=cur.execute('SELECT phone_user FROM user WHERE user_id=(?) and NOT phone_user="Null";',(user_id,)).fetchone()[0]
    print(kek)

    return kek



async def db_uslugi(): #получить все услуги
    all_uslug=cur.execute("SELECT * FROM uslugi").fetchall()
    return all_uslug

async def db_all_uslugi(nazvanie): #запрос на получение под услуг
    all_uslug=cur.execute('SELECT * FROM all_uslugi WHERE nazvanie=(?);',(nazvanie,)).fetchall()
    return all_uslug

async def price_all_uslgugi(nazvanie): #получение стоимости финальной услуги для вывода в сообщение пользователя
    all_uslug=cur.execute('SELECT price_uslugi FROM all_uslugi WHERE name_uslugi=(?);',(nazvanie,)).fetchall()
    return all_uslug

async def get_time_uslug(time_date,usluga): #получить окошки
    all_uslug=cur.execute("SELECT time_u FROM time_uslugi WHERE date_u=(?) and name_u='' and user_id='';",(time_date,)).fetchall() #юзер ид пробел, проверка чтобы только не записанные
    return all_uslug

async def zapis_final(user_id,user_name,user_phone,date_u,time_u,name_u): #запись на прием
    zapis = cur.execute("""UPDATE time_uslugi SET name_u=(?), user_id=(?),user_name=(?), user_phone=(?) WHERE date_u=(?) and time_u=(?);""", (name_u, user_id, user_name, user_phone, date_u, time_u))
  #  zapis=cur.execute("""UPDATE time_uslugi SET user_id=(?),user_name=(?),user_phone=(?) WHERE date_u=(?) and time_u=(?) and name_u=(?);""",(user_id,user_name,user_phone,date_u,time_u,name_u))
    db.commit()
    return zapis

async def zapis_final2(user_id,user_name,user_phone,date_u,time_u,name_u): #запись на прием #если у пользователя уже сохранен номер в базе(уже записывался)
    zapis=cur.execute("""UPDATE time_uslugi SET name_u=(?), user_id=(?),user_name=(?), user_phone=(?) WHERE date_u=(?) and time_u=(?);""",(name_u,user_id,user_name,user_phone,date_u,time_u))
    db.commit()
    return zapis


####################################кнопка мои записии##################################

async def get_zapis(user_id1): #получение всех усдуг на которые записан типо
    all_uslug = cur.execute("SELECT * FROM time_uslugi WHERE user_id=(?) and date(date_u)>=(?);", (user_id1,datetime.date.today())).fetchall() #запрос на получение всех записей которые еще не прошли
    return all_uslug

async def get_one_zapis(date_id): #получение записи которую пользователь выбрал по дате ид
    all_uslug = cur.execute("SELECT * FROM time_uslugi WHERE date_id=(?);", (date_id,)).fetchone() #запрос на получение всех записей которые еще не прошли
    return all_uslug

async def delet_zapis(date_id): #удаление пользователя из записи
    all_uslug=cur.execute('UPDATE time_uslugi SET user_id="",name_u="",user_name="",user_phone="" WHERE date_id=(?);',(date_id,))
    db.commit()
    return all_uslug

async def update_phone(user_phone,user_id):
    all_uslug=cur.execute('UPDATE time_uslugi SET user_phone=(?) WHERE user_id=(?)',(user_phone,user_id))
    db.commit()
    print('Обновилось первое')
    kek=cur.execute('UPDATE user SET phone_user=(?) WHERE user_id=(?)',(user_phone,user_id))
    db.commit()
    return all_uslug
async def update_name(user_name,user_id):
    all_uslug=cur.execute('UPDATE time_uslugi SET user_name=(?) WHERE user_id=(?)',(user_name,user_id))
    db.commit()
    print('Обновилось первое')
    kek=cur.execute('UPDATE user SET last_name=(?) WHERE user_id=(?)',(user_name,user_id))
    db.commit()
    return all_uslug
async def user_name(user_phone,user_id):
    all_uslug=cur.execute('UPDATE user SET last_name=(?) WHERE user_id=(?)',(user_phone,user_id))
    db.commit()

async def get_name(user_id):
    all_uslug=cur.execute('SELECT last_name FROM user WHERE user_id=(?)',(user_id,)).fetchone()[0]
    return all_uslug

################################admink_excel################################
async def take_users_id():
    all_uslug=cur.execute('SELECT user_id from user').fetchall()
    print(all_uslug)
    return all_uslug

async def do_date(date_u,time_u): #запрос на добавление из екселя
    cur.execute('INSERT INTO time_uslugi(date_u,time_u,name_u,user_id) VALUES (?,?,?,?);', (date_u, time_u,'',''))
    db.commit()

async def take_zapisanie():
      all_uslug=cur.execute('SELECT date_u from time_uslugi;').fetchall()
      print(all_uslug)
      return all_uslug

async def delet_ne_zapisanie():
    cur.execute('DELETE FROM time_uslugi WHERE user_id="";')
    db.commit()

async def insert_uslugi(nazvanie):
    cur.execute('INSERT INTO uslugi(nazvanie_uslugi) VALUES (?);',(nazvanie,))
    db.commit()

async def insert_alluslugi(nazvanie,n_uslugi,p_uslugi):
    cur.execute('INSERT INTO all_uslugi(nazvanie,name_uslugi,price_uslugi) VALUES (?,?,?);',(nazvanie,n_uslugi,p_uslugi))
    db.commit()

async def delet_uslugi():
    cur.execute('DELETE FROM uslugi;')
    cur.execute('DELETE FROM all_uslugi')
    db.commit()


################################admin################################



async def take_show_zapisi(): #выбор уникальных данных из таблицы time_uslugi
    all_uslug=cur.execute('SELECT DISTINCT date_u FROM time_uslugi WHERE date(date_u)>=(?);',(datetime.date.today(),)).fetchall()
    return all_uslug

async def take_show_time(date_u): #получаем дата ид время по дате
    all_uslug=cur.execute('SELECT date_id,time_u,user_id from time_uslugi WHERE date_u=(?);',(date_u,)).fetchall()
    return all_uslug

async def delet_po_time(date_id):
    cur.execute('DELETE FROM time_uslugi WHERE date_id=(?);',(date_id,))
    db.commit()

async def delet_po_zapisi(user_id):
    cur.execute('DELETE FROM time_uslugi WHERE user_id=(?);',(user_id,))
    db.commit()


async def delet_daty(date_):
    cur.execute('DELETE FROM time_uslugi WHERE date_u=(?);', (date_,))
    db.commit()

async def count_daty(date_u): #счет есть ли в запросе выше польвотели
    all_uslug = cur.execute("SELECT COUNT(*) FROM time_uslugi WHERE date_u=(?) and NOT user_id=''",(date_u,)).fetchone()[0]
    print(all_uslug)
    return all_uslug

async def take_zapisi_people(): #выбор уникальных данных из таблицы time_uslugi
    all_uslug=cur.execute('SELECT DISTINCT user_id,user_name,user_phone FROM time_uslugi').fetchall()
    return all_uslug

async def delete_starie():
    all_uslug=cur.execute('DELETE FROM time_uslugi  WHERE date(date_u)<(?);',(datetime.date.today(),))
    db.commit()

async def take_username(id):
    all_uslug=cur.execute('SELECT username FROM user WHERE user_id=(?);',(id,)).fetchone()[0]
    return all_uslug


async def take_uslug(nazvanie):
    all_uslug=cur.execute('SELECT * FROM all_uslugi WHERE nazvanie=(?);',(nazvanie,)).fetchall()
    return all_uslug

async def get_usluga(id):
    all_uslug = cur.execute('SELECT * FROM all_uslugi WHERE id=(?);', (id,)).fetchall()
    return all_uslug

async def delet_usluga(id):
    all_uslug = cur.execute('DELETE FROM all_uslugi WHERE id=(?);', (id,))
    db.commit()

async def update_usluga(id,mess):
    all_uslug = cur.execute('UPDATE all_uslugi SET price_uslugi=(?) WHERE id=(?);', (id,mess))
    db.commit()



#######################конфиг прочее бд №№№№№№№№№№№№№№№№№№

async def get_location():
    all_uslug=cur.execute('SELECT glav FROM config').fetchone()[0]
    return all_uslug

async def give_location(opis):
    all_uslug=cur.execute('UPDATE config SET glav=(?) WHERE information="1"',(opis,))
    db.commit()

async def get_opisanie():
    all_uslug=cur.execute('SELECT photo FROM config').fetchone()[0]
    return all_uslug

async def infa(opis):
    all_uslug=cur.execute('UPDATE config SET photo=(?) WHERE information="1"',(opis,))
    db.commit()

async def get_baza(): #получить все услуги
    all_uslug=cur.execute("SELECT * FROM user").fetchall()
    return all_uslug
