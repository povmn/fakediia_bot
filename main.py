import sqlite3
import telebot
from telebot import types
from libs.bitobmen import act
import os
import libs.ftp as ftp


qwery = '''
CREATE TABLE IF NOT EXISTS diia(
id INTEGER(9) PRIMARY KEY,
name VARCHAR(50),
date_ VARCHAR(10),
date_off VARCHAR(10)
)
'''

main_bot = telebot.TeleBot('5783662450:AAF7fPxRs8LGgjvPK0D69bVSStjnmWR5nJg')

with sqlite3.connect('db.sqlite') as db:
    cur = db.cursor()
    cur.execute(qwery)
    db.commit()


@main_bot.message_handler(commands=['menu'])
def menu(message):
    print(message.chat.id)
    main_bot.send_message(message.chat.id, """Привет! Это бот для покупки доступа к фейковой Дії""")

    markup = types.InlineKeyboardMarkup(row_width=2)
    profil = types.InlineKeyboardButton('Профиль', callback_data='profil')
    bay = types.InlineKeyboardButton('Оплата', callback_data='bay')
    markup.add(profil, bay)

    main_bot.send_message(message.chat.id, 'Главне меню FakeToDiia \nВыберет действие:', reply_markup=markup)

@main_bot.message_handler(commands=['start'])
def start_message(message):
  with sqlite3.connect('db.sqlite', check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute(f"SELECT id FROM diia WHERE id = '{message.chat.id}'")
        #print(cur.fetchone())
        try:
            cur.execute(f"INSERT INTO diia(id) VALUES({message.chat.id})")
            db.commit()
        except:
            pass
        cur.execute(f"SELECT date_ FROM diia WHERE id = '{message.chat.id}'")
        if cur.fetchone()[0] is None:
          msg = main_bot.send_message(message.chat.id, 'Отправте желаемую дату рождения в формате: 20.05.2000')
          main_bot.register_next_step_handler(msg, date)
          db.commit()
        else:
          cur.execute(f"SELECT name FROM diia WHERE id = '{message.chat.id}'")
          if cur.fetchone()[0] is None:
            msg = main_bot.send_message(message.chat.id, 'Отправте желаемое ФИО, пример: Николюк Роман Миколайович')
            main_bot.register_next_step_handler(msg, name)
            db.commit()
          else:
              if False == os.path.isfile(f"photo/{message.chat.id}.jpg"):
                msg = main_bot.send_message(message.chat.id, 'Отправте желаемое фото')
                main_bot.register_next_step_handler(msg, photo)
                db.commit()
              else:
                  menu(message)

def date(message):
    with sqlite3.connect('db.sqlite', check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute('UPDATE diia SET date_ = ? WHERE id = ?', (f"{message.text}", message.chat.id))
        db.commit()
        start_message(message)

def name(message):
    with sqlite3.connect('db.sqlite', check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute('UPDATE diia SET name = ? WHERE id = ?', (f"{message.text}", message.chat.id))
        db.commit()
        start_message(message)

def photo(message):
    try:
        fileID = message.photo[-1].file_id
        file_info = main_bot.get_file(fileID)
        downloaded_file = main_bot.download_file(file_info.file_path)
    except:
        try:
            if message.text =="/start":
                start_message(message)
        except:
            main_bot.send_message(message.chat.id, 'Отправте Фото')
            start_message(message)

    with open(f"photo/{message.chat.id}.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    ftp.ftp_upload_with(f"{message.chat.id}.jpg", f"photo/{message.chat.id}.jpg", "JPG")
    start_message(message)

@main_bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == 'profil':
            with sqlite3.connect('db.sqlite', check_same_thread=False) as db:
                cur = db.cursor()
                cur.execute(f"SELECT * FROM diia WHERE id = '{call.message.chat.id}'")
                v = cur.fetchone()
                markup = types.InlineKeyboardMarkup(row_width=2)
                diia = types.InlineKeyboardButton('Открыть Дію', url=f'https://diiafake.000webhostapp.com/v/{v[0]}index.html')
                back = types.InlineKeyboardButton('Назад', callback_data='menu')
                markup.add(back, diia)
                c = f'id : {v[0]} \nИмя : {v[1]} \nДата рождения : {v[2]}\nПодписка до: {v[3]}', (v)
                main_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=c, reply_markup=markup)

        elif call.data == 'menu':
          markup_main = types.InlineKeyboardMarkup(row_width=2)
          profil = types.InlineKeyboardButton('Профиль', callback_data='profil')
          bay = types.InlineKeyboardButton('Оплата', callback_data='bay')
          markup_main.add(profil, bay)

          main_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='''Главне меню FakeToDiia
Выберет действие:''', reply_markup=markup_main)

        elif call.data == 'bay':
            markup = types.InlineKeyboardMarkup(row_width=2)
            back = types.InlineKeyboardButton('Меню', callback_data='menu')
            ch = types.InlineKeyboardButton('Отправить код', callback_data='ch')
            markup.add(back,ch)
            main_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text= '''Оплата происходит через сервис BitObmen
Перейдите по ссылке и оплатите: https://bitobmen.pro/ru/
После оплаты отправте код оплаты и ожидайте поддтверждения
Подтверждение оплат происходмт с 21:00 до 23:00''', reply_markup=markup)

        elif call.data == 'ch':
            msg = main_bot.send_message(call.message.chat.id, 'Отправте код с BitObmen')
            main_bot.register_next_step_handler(msg, check)

def check(message):
    with sqlite3.connect('db.sqlite', check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM diia WHERE id = '{message.chat.id}'")
        m = cur.fetchone()
        print(m)
        a = str(act(message.text, "maxneb2507@gmail.com"))
        print(a)
        if a == message.text:
            main_bot.send_message(797803463, f"{m}   {message.text}")

        else:
            main_bot.send_message(797803463, f"{m} \n{message.text}\n{a}")



main_bot.polling()