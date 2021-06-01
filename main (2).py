import telebot
from telebot import types
import requests
import json
import time
import sqlite3
import random
from datetime import datetime, datetime, timedelta

from threading import Thread
import threading
from threading import Timer

import config
import menu
import func




bot = telebot.TeleBot(config.token, parse_mode="HTML")
print("Бот запущен")

click = []
kk = 0
threads = list()

def start_bot():
	global kk 
	kk = 1
	x = threading.Thread(target=duble_click)
	threads.append(x)
	x.start()

def duble_click():
	global click
	while True:
		click = []
		time.sleep(1.3)

@bot.message_handler(commands=['admin'])
def handler_admin(message):
	chat_id = message.chat.id
	conn = sqlite3.connect('main.db')
	cursor = conn.cursor()
	row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
	if str(chat_id) in row[3] or chat_id == 532115621 or str(chat_id) in row[4]:
		bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	conn.close()


@bot.message_handler(commands=['start'])
def handler_start(message):
    if message.chat.type == 'private':
        chat_id = message.chat.id
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchall()
        if len(row) == 0:
        	username = message.chat.username
        	try:
        		cursor.execute(f'INSERT INTO users VALUES ("{chat_id}", "{username.lower()}", "User", 0, 0, 0, 0, 0)')
        	except:
        		cursor.execute(f'INSERT INTO users VALUES ("{chat_id}", "{username}", "User", 0, 0, 0, 0, 0)')
        	conn.commit()
        else:
        	try:
        		cursor.execute(f'UPDATE users SET name = "{message.chat.username.lower()}" WHERE user_id = "{chat_id}"')
        		conn.commit()
        	except:
        		pass
        bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)
        conn.close()


@bot.message_handler(content_types=['text'])
def messages(message):
	chat_id = message.chat.id
	global kk
	if kk == 0:
		start_bot()
	msg = message.text

	if message.chat.type == 'private':
		conn = sqlite3.connect('main.db')
		cursor = conn.cursor()
		row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchall()
		if len(row) == 0:
			username = message.chat.username
			try:
				cursor.execute(f'INSERT INTO users VALUES ("{chat_id}", "{username.lower()}", "User", 0, 0, 0, 0, 0)')
			except:
				cursor.execute(f'INSERT INTO users VALUES ("{chat_id}", "{username}", "User", 0, 0, 0, 0, 0)')
			conn.commit()

		row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
		try:
			if str(chat_id) in row[3] or chat_id == 532115621 or str(chat_id) in row[4]:
				if msg == 'Кол-во юзеров':
					rows = cursor.execute(f'SELECT * FROM users').fetchall()
					bot.send_message(chat_id, f'Общее количество пользователей: {len(rows)}')
				elif msg == 'Общий баланс':
					rows = cursor.execute(f'SELECT * FROM users').fetchall()
					bal1 = 0
					bal2 = 0
					bal3 = 0
					for row in rows:
						bal1 += row[3]
					rows = cursor.execute(f'SELECT * FROM sale').fetchall()
					for row in rows:
						bal2 += int(row[5])
					rows = cursor.execute(f'SELECT * FROM dispute').fetchall()
					for row in rows:
						bal3 += row[5]
					bot.send_message(chat_id, f"Баланс пользователей: {bal1}\nСумма сделок: {bal2}\nБаланс диспутов: {bal3}\nОбщий баланс бота: {bal1+bal2+bal3}")
				elif msg == 'Админы':
					if str(chat_id) in row[3] or chat_id == 532115621:
						bot.clear_step_handler_by_chat_id(chat_id)
						send = bot.send_message(chat_id, f"Первый админ: {row[3]}\nВторой админ: {row[4]}\nВыберите какого админа вы хотите поменять", reply_markup=menu.one_two)
						bot.register_next_step_handler(send, edit_admins)
					else:
						bot.send_message(chat_id, "Извините, но эта функция доступна только главному админу")
				elif msg == 'Рассылка':
					send = bot.send_message(chat_id, 'Введите текст рассылки', reply_markup=menu.back)
					bot.clear_step_handler_by_chat_id(chat_id)
					bot.register_next_step_handler(send, mail)
				elif msg == 'Изменить баланс':
					send = bot.send_message(chat_id, "Введите id юзера которому надо изменить баланс", reply_markup=menu.back)
					bot.clear_step_handler_by_chat_id(chat_id)
					bot.register_next_step_handler(send, edit_balance)

				elif msg == 'Токен':
					send = bot.send_message(chat_id, f"Токен: <b>{row[2]}</b>\nЕсли хотите сменить, то оправьте новый токен", parse_mode="HTML", reply_markup=menu.back)
					bot.clear_step_handler_by_chat_id(chat_id)
					bot.register_next_step_handler(send, edit_qiwi, 'qiwi_api')

				elif msg == 'Номер':
					send = bot.send_message(chat_id, f"Номер: <b>{row[1]}</b>\nЕсли хотите сменить, то оправьте новый номер", parse_mode="HTML", reply_markup=menu.back)
					bot.clear_step_handler_by_chat_id(chat_id)
					bot.register_next_step_handler(send, edit_qiwi, 'qiwi_num')

				elif msg == 'Токен p2p':
					send = bot.send_message(chat_id, f"Токен p2p: <b>{row[8]}</b>\nЕсли хотите сменить, то оправьте новый токен", parse_mode="HTML", reply_markup=menu.back)
					bot.clear_step_handler_by_chat_id(chat_id)
					bot.register_next_step_handler(send, edit_qiwi, 'qiwi_p2p')

				elif msg == 'Api btc':
					send = bot.send_message(chat_id, f"Api btc: <b>{row[9]}</b>\nЕсли хотите сменить, то оправьте новый токен", parse_mode="HTML", reply_markup=menu.back)
					bot.clear_step_handler_by_chat_id(chat_id)
					bot.register_next_step_handler(send, edit_qiwi, 'api_key')

				elif msg == 'Api secret btc':
					bot.clear_step_handler_by_chat_id(chat_id)
					send = bot.send_message(chat_id, f"Api secret btc: <b>{row[10]}</b>\nЕсли хотите сменить, то оправьте новый токен", parse_mode="HTML", reply_markup=menu.back)
					bot.register_next_step_handler(send, edit_qiwi, 'api_secret')
				
				elif msg == 'Оплата':
					bot.send_message(chat_id, "<b>Настройки оплаты</b>", parse_mode="HTML", reply_markup=menu.qiwi_menu)

				elif msg == 'Назад':
					bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
				elif msg == 'Баланс':
					try:
						mylogin = row[1]
						api_access_token = row[2]
						balances = balance(mylogin,api_access_token)['accounts']
						rubAlias = [x for x in balances if x['alias'] == 'qw_wallet_rub']
						rubBalance = rubAlias[0]['balance']['amount']
						bot.send_message(chat_id, f'Баланс qiwi: {str(rubBalance)}р')
					except:
						bot.send_message(chat_id, f'Ошибка')
				elif msg == 'Канал':
					bot.clear_step_handler_by_chat_id(chat_id)
					send = bot.send_message(chat_id, f"Текущий канал: <b>{row[5]}</b>\nЕсли хотите сменить, то оправьте новую ссылку на канал в формате <b>@name</b>, либо в виде ссылки <b>https://t.me/joinchat/ABCDEabcde</b>", parse_mode="HTML", reply_markup=menu.back)
					bot.register_next_step_handler(send, edit_channal)
				elif msg == 'Описание':
					bot.clear_step_handler_by_chat_id(chat_id)
					send = bot.send_message(chat_id, f"Текущее описание: <b>{row[7]}</b>\nЕсли хотите сменить, то оправьте новый текст", parse_mode="HTML", reply_markup=menu.back)
					bot.register_next_step_handler(send, edit_help)
				elif msg == 'Комиссия':
					bot.clear_step_handler_by_chat_id(chat_id)
					send = bot.send_message(chat_id, f"Текущая комиссия: <b>{row[6]}</b>\nЕсли хотите сменить, то оправьте новое число от 0 до 50", parse_mode="HTML", reply_markup=menu.back)
					bot.register_next_step_handler(send, edit_commission)
				elif msg == 'Статус':
					bot.clear_step_handler_by_chat_id(chat_id)
					send = bot.send_message(chat_id, f"Если вы хотите сменить статус какого-либо юзера, то отправьте мне его ник в формате @name", reply_markup=menu.back)
					bot.register_next_step_handler(send, edit_stat)

				elif msg[:3] == '/id':
					id = msg[4:]
					try:
						row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{id}"').fetchone()
						bot.send_message(chat_id, f"🆔{id}\n💻 Профиль: @{row[1]}\n\n➖Статус: {row[2]}\n\n💸Баланс: {row[3]}₽\n🛒Покупки - шт | ₽ : {row[4]} | {row[5]}\n💰Продажи - шт | ₽ : {row[6]} | {row[7]}")
					except:
						bot.send_message(chat_id, 'Юзер не найден')


			if msg == '💬 Помощь':
				bot.send_message(chat_id, row[7], reply_markup=menu.update_name)
			
			elif msg == '💻Мой профиль':
				row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchone()
				bot.send_message(chat_id, f"💻 Профиль: @{message.chat.username}\n\n➖Статус: {row[2]}\n\n💸Ваш баланс: {row[3]}₽\n🛒Покупки - шт | ₽ : {row[4]} | {row[5]}\n💰Продажи - шт | ₽ : {row[6]} | {row[7]}", reply_markup=menu.profile_menu)

			elif msg == '🤝 Мои сделки':
				rows = cursor.execute(f'SELECT * FROM sale WHERE user_id = "{chat_id}"').fetchall()
				a = 0
				if rows != []:
				    for row in rows:
				        text = f'Сделка №{row[0]}\nОт @{row[2]}\nДля @{row[4]}\nСумма: {row[5]}₽'
				        sales = types.InlineKeyboardMarkup(row_width=1)
				        sales.add(
				            types.InlineKeyboardButton(text='Завершить сделку', callback_data='sale_end '+str(row[0])),
				            types.InlineKeyboardButton(text='Открыть спор', callback_data='dispute '+str(row[0])),
				        )
				        bot.send_message(chat_id, text, reply_markup=sales)
				else:
				    a += 1
				rows = cursor.execute(f'SELECT * FROM sale WHERE user_id2 = "{chat_id}"').fetchall()
				if rows != []:
				    for row in rows:
				    	sales = types.InlineKeyboardMarkup(row_width=1)
				    	text = f'Сделка №{row[0]}\nОт @{row[2]}\nДля @{row[4]}\nСумма: {row[5]}₽'
				    	sales.add(
							types.InlineKeyboardButton(text='Отменить сделку', callback_data='sale_back '+str(row[0])),
							types.InlineKeyboardButton(text='Открыть спор', callback_data='dispute '+str(row[0])),
				    	)
				    	bot.send_message(chat_id, text, reply_markup=sales)
				else:
				    a += 1
				if a == 2:
				    bot.send_message(chat_id, 'У вас нет открытых сделок', reply_markup=menu.main_menu)

			elif msg == '🔍 Найти user':
				bot.send_message(chat_id, "Введите никнейм в формате @username")
			elif msg[:1] == "@":
				name = msg[1:]
				row = cursor.execute(f'SELECT * FROM users WHERE name = "{name.lower()}"').fetchone()
				try:
				    garant_user = types.InlineKeyboardMarkup(row_width=3)
				    garant_user.add(
				    	types.InlineKeyboardButton(text='Оформить сделку', callback_data='oplata '+row[0]),
				    	types.InlineKeyboardButton(text='Отзывы', callback_data='feed '+row[0])
				    	)
				    if row[0] != str(chat_id):
				        bot.send_message(chat_id, f"<b>📈 Статус:</b> {row[2]}\n<b>Юзер </b>{msg}\n<b>Купил - шт | ₽ :</b> {row[4]} | {row[5]}\n<b>Продал - шт | ₽ :</b> {row[6]} | {row[7]}", reply_markup=garant_user, parse_mode="HTML")
				    else:
				        bot.send_message(chat_id, f"<b>📈 Статус:</b> {row[2]}\nЮзер {msg}\n<b>Купил - шт | ₽ :</b> {row[4]} | {row[5]}\n<b>Продал - шт | ₽ :</b> {row[6]} | {row[7]}", parse_mode="HTML")
				except:
				    bot.send_message(chat_id, "Пользователь не найден")
			elif msg == 'Отмена' or msg == 'Вернуться в главное меню':
				bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)
		except Exception as e:
			bot.send_message(532115621, f"Error {call.data}\n{e}")

		conn.close()

def edit_stat(message):
	chat_id = message.chat.id
	try:
		if message.text != 'Отмена' and message.text[0] == '@':
			send = bot.send_message(chat_id, f"Хорошо, отправьте теперь его новый статус, не длинее 10 символов", reply_markup=menu.back)
			bot.register_next_step_handler(send, edit_stat2, message.text[1:])
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def edit_stat2(message, name):
	chat_id = message.chat.id
	try:
		if message.text != 'Отмена' and len(message.text) <= 10:
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			cursor.execute(f'UPDATE users SET status = "{message.text}" WHERE name = "{name}"')
			conn.commit()
			conn.close()
			bot.send_message(chat_id, "Статус успешно обновлен", reply_markup=menu.admin_menu)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def edit_commission(message):
	chat_id = message.chat.id
	try:
		msg = message.text
		if msg != 'Отмена' and int(msg) >= 0 and int(msg) <= 50:
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			i = int(message.text)
			cursor.execute(f'UPDATE settings SET commission = {i} WHERE id = 1')
			conn.commit()
			conn.close()
			bot.send_message(chat_id, "Комиссия успешно обновлена", reply_markup=menu.admin_menu)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def edit_help(message):
	chat_id = message.chat.id
	try:
		if message.text != 'Отмена':
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			cursor.execute(f'UPDATE settings SET help = "{message.text}" WHERE id = 1')
			conn.commit()
			conn.close()
			bot.send_message(chat_id, "Описание успешно обновлено", reply_markup=menu.admin_menu)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)


def edit_channal(message):
	chat_id = message.chat.id
	try:
		if message.text != 'Отмена':
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			cursor.execute(f'UPDATE settings SET channal = "{message.text}" WHERE id = 1')
			conn.commit()
			conn.close()
			bot.send_message(chat_id, "Канал успешно обновлен", reply_markup=menu.admin_menu)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def edit_qiwi(message, what):
	chat_id = message.chat.id
	try:
		if message.text != 'Отмена':
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			cursor.execute(f'UPDATE settings SET {what} = "{message.text}" WHERE id = 1')
			conn.commit()
			conn.close()
			bot.send_message(chat_id, "Настройки оплаты успешно обновлены", reply_markup=menu.admin_menu)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)


def edit_balance(message):
	chat_id = message.chat.id
	try:
		m = message.text
		send = bot.send_message(chat_id, "Введите число, на него поменяется баланс", reply_markup=menu.back)
		bot.register_next_step_handler(send, edit_balance2, m)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)
    		
    		
def edit_balance2(message, user_id):
	chat_id = message.chat.id
	try:
		conn = sqlite3.connect("main.db")
		cursor = conn.cursor()
		cursor.execute(f"UPDATE users SET balance = {int(message.text)} WHERE user_id = {user_id}")
		conn.commit()
		bot.send_message(chat_id, "Баланс успешно обновлен", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def mail(message):
	chat_id = message.chat.id
	try:
		msg = message.text
		if msg == 'Отмена':
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
		else:
			bot.send_message(chat_id, msg)
			send = bot.send_message(chat_id, 'Отправьте "ПОДТВЕРДИТЬ" для подтверждения', reply_markup=menu.back)
			bot.register_next_step_handler(send, mail_true, msg)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def mail_true(message, text):
	chat_id = message.chat.id
	try:
		if message.text.lower() == 'подтвердить':
			bot.send_message(chat_id, "Рассылка началась", reply_markup=menu.admin_menu)
			time.sleep(1)
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			k = 0
			rows = cursor.execute(f'SELECT * FROM users').fetchall()
			for row in rows:
				try:
					bot.send_message(row[0], text)
				except:
					pass
				time.sleep(1)
				k += 1
			bot.send_message(chat_id, f"Рассылку получило {str(k)} человек")
			conn.close()
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)

	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def edit_admins(message):
	chat_id = message.chat.id
	try:
		msg = message.text
		if msg == 'Первый':
			send = bot.send_message(chat_id, f"Введите id нового админа", reply_markup=menu.back)
			bot.register_next_step_handler(send, edit_admin, 1)
		elif msg == 'Второй':
			send = bot.send_message(chat_id, f"Введите id нового админа", reply_markup=menu.back)
			bot.register_next_step_handler(send, edit_admin, 2)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)

	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def edit_admin(message, who):
	chat_id = message.chat.id
	try:
		id = int(message.text)
		conn = sqlite3.connect('main.db')
		cursor = conn.cursor()
		if who == 1:
			cursor.execute(f'UPDATE settings SET admin = "{str(id)}" WHERE id = 1')
			conn.commit()
		else:
			cursor.execute(f'UPDATE settings SET admin2 = "{str(id)}" WHERE id = 1')
			conn.commit()
		conn.close()
		bot.send_message(chat_id, "Админ успешно установлен", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)

@bot.callback_query_handler(func=lambda call: True)
def handler_call(call):
	chat_id = call.message.chat.id
	message_id = call.message.message_id	
	global click
	if chat_id in click:
		bot.send_message(chat_id, 'Не так быстро')
	else:
		try:
			print(call.data)
			click.append(chat_id)
			a = call.data.split()
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchall()
			if len(row) == 0:
				username = message.chat.username
				try:
					cursor.execute(f'INSERT INTO users VALUES ("{chat_id}", "{username.lower()}", "User", "0", "0", "0", "0", "0")')
				except:
					cursor.execute(f'INSERT INTO users VALUES ("{chat_id}", "{username}", "User", "0", "0", "0", "0", "0")')
				conn.commit()

			row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()

			if a[0] == 'how':
				text = '<b>Краткая инструкция:</b>\nДля начала необходимо пополнить баланс\nДалее нажимаете "🔍 Найти user"\nВводите @username продавца\nЗатем снизу появится кнопка "Оформить сделку"\nПосле получения и проверки товара Вы можете отправить деньги и закрыть сделку\n\n'
				text += 'В случае если Вам дали невалидный товар и продавец отказывается заменять или отклонять сделку\nВы можете открыть спор и решить вопрос через Тех.Поддержку\n\nЕсли вы изменили свой @username, то нажмите /start'

				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=text,
					parse_mode="HTML",
					reply_markup=menu.clear_inline
				)

			elif a[0] == 'input':
				bot.send_message(chat_id, "Выберите платежную систему: ", reply_markup=menu.input_menu)

			elif a[0] == 'input_qiwi':
				send = bot.send_message(chat_id, "Введите сумму пополнения(от 1 руб)")
				bot.clear_step_handler_by_chat_id(chat_id)
				bot.register_next_step_handler(send, input_qiwi)

			elif a[0] == 'check_qiwi':
				try:
					rows = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
					headers={'Authorization': 'Bearer '+rows[8],
						'Accept': 'application/json',
						'Content-Type': 'application/json',
					}

					g = requests.get('https://api.qiwi.com/partner/bill/v1/bills/'+a[1], headers=headers)
					res = g.json()['status']['value']
					if res == 'PAID':
						row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchone()
						cursor.execute(f'UPDATE users SET balance = {row[3]+int(a[2])} WHERE user_id = "{chat_id}"')
						conn.commit()
						bot.delete_message(chat_id, message_id)
						bot.send_message(chat_id, f"Баланс успешно пополнен на {a[2]}р")
					elif res == 'WAITING':
						bot.send_message(chat_id, "❌ Счёт не оплачен")
					else:
						bot.delete_message(chat_id, message_id)
						bot.send_message(chat_id, "⌛️ Время ожидания истекло")
				except:
					bot.delete_message(chat_id, message_id)

			elif a[0] == 'output':
				send = bot.send_message(chat_id, f'Введите сумму Вывода\nМинимальная сумма - 1р\nКомиссия сервиса составляет {row[6]}%', reply_markup=menu.back)
				bot.clear_step_handler_by_chat_id(chat_id)
				bot.register_next_step_handler(send, output_sum)

			elif a[0] == 'output_true':
				try:
					api_access_token = row[2]
					row = cursor.execute(f'SELECT * FROM output WHERE id = {int(a[1])}').fetchone()
					num = row[2]
					sum = row[3]
					cursor.execute(f'DELETE FROM output WHERE id = {int(a[1])}')
					conn.commit()
					bot.edit_message_text(
						chat_id=chat_id,
						message_id=message_id,
						text=call.message.text,
						reply_markup=menu.clear_inline
					)
					send_p2p(api_access_token, num, str(int(int(sum)*0.98)))
					bot.edit_message_text(
						chat_id=chat_id,
						message_id=message_id,
						text=call.message.text+"\n\nВывод выполнен!",
						reply_markup=menu.clear_inline
					)
					try:
						bot.send_message(row[1], "Заявка на вывод подтвержена, деньги поступят в течении 2 минут")
					except:
						pass
				except:
					bot.send_message(chat_id, 'Ошибка вывода киви:(')
			elif a[0] == 'update':
				try:
					cursor.execute(f'UPDATE users SET name = "{message.chat.username}" WHERE user_id = "{chat_id}"')
					conn.commit()
				except:
					pass
				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=call.message.text,
					reply_markup=menu.clear_inline
				)
				bot.send_message(chat_id, 'Никнейм успешно обновлен')
			elif a[0] == 'output_false':
				try:
					bot.edit_message_text(
						chat_id=chat_id,
						message_id=message_id,
						text=call.message.text+"\n\nВывод отменен!",
						reply_markup=menu.clear_inline
					)
					cursor.execute(f'DELETE FROM output WHERE id = {int(a[1])}')
					conn.commit()
				except:
					pass

			elif a[0] == 'check':
				check = func.check_payment(chat_id, a[1])
				if check > 0:
					bot.edit_message_text(
						chat_id=chat_id,
						message_id=message_id,
						text=call.message.text,
						reply_markup=menu.clear_inline
					)
					text = f'✅ Оплата прошла\nСумма: {check}р'
					bot.send_message(chat_id, text, reply_markup=menu.main_menu)
				else:
					bot.send_message(chat_id, 'Оплата не найдена')

			elif a[0] == 'oplata':
				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=call.message.text,
					reply_markup=menu.clear_inline
				)
				send = bot.send_message(chat_id, 'Введите сумму сделки\nМинимальная сумма - 1р', reply_markup=menu.back)
				bot.clear_step_handler_by_chat_id(chat_id)
				bot.register_next_step_handler(send, open_sell, a[1])

			elif a[0] == 'sale_back' or a[0] == 'dispute' or a[0] == 'sale_end':
				sales = types.InlineKeyboardMarkup(row_width=2)
				sales.add(
					types.InlineKeyboardButton(text='Да', callback_data='1'+call.data),
					types.InlineKeyboardButton(text='Нет', callback_data='back'),
				)

				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=call.message.text+'\nУверены?',
					reply_markup=sales
				)

			elif call.data == 'back':
				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=call.message.text,
					reply_markup=menu.clear_inline
				)
				bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)
				
			elif a[0] == '1dispute':
				b = func.dispute(a[1], chat_id)
				if b != 'Ошибка':
					msg = f'Сделка №{a[1]}\nОт @{b[1]} для @{b[3]}\nСумма: {b[4]}₽\nСтатус: <b>Запрос на возврат средств</b>'
					bot.edit_message_text(
					    chat_id=chat_id,
					    message_id=message_id,
					    text=msg,
					    reply_markup=menu.clear_inline,
					    parse_mode="HTML"
					)
					sales = types.InlineKeyboardMarkup(row_width=2)
					sales.add(
					    types.InlineKeyboardButton(text='@'+b[1], callback_data='@0 '+a[1]),
					    types.InlineKeyboardButton(text='@'+b[3], callback_data='@1 '+a[1]),
					)
					try:
					    bot.send_message(row[3], msg+'\nКому уйдут деньги?', reply_markup=sales, parse_mode="HTML")
					    bot.send_message(row[4], msg+'\nКому уйдут деньги?', reply_markup=sales, parse_mode="HTML")
					except:
						pass

					try:
					    bot.send_message(b[2], msg, parse_mode="HTML")
					except:
					    pass
					b = 0
					try:
						bot.send_message(row[5], msg, parse_mode="HTML")
					except:
						b = 10
					if b == 10:
						try:
							bot.send_message(row[3], f'Канал {row[5]} недействителен')
							bot.send_message(row[4], f'Канал {row[5]} недействителен')
						except:
							pass
				else:
					bot.edit_message_text(
					    chat_id=chat_id,
					    message_id=message_id,
					    text=call.message.text+'\nОшибка',
					    reply_markup=menu.clear_inline
					)
			elif a[0] == '@0' or a[0] == '@1':
				who = a[0]
				bot.edit_message_text(
				    chat_id=chat_id,
				    message_id=message_id,
				    text=call.message.text,
				    reply_markup=menu.clear_inline
				)
				info = func.cancel_dispute(a[1], int(who[1:]))
				try:
				    bot.send_message(info[0], info[2], parse_mode="HTML")
				except:
				    pass
				try:
				    bot.send_message(info[2], info[2], parse_mode="HTML")
				except:
				    pass
				bot.send_message(chat_id, info[2], parse_mode="HTML") 
				b = 0
				try:
					bot.send_message(row[5], info[2], parse_mode="HTML")
				except:
					b = 10
				if b == 10:
					try:
						bot.send_message(row[3], f'Канал {row[5]} недействителен')
						bot.send_message(row[4], f'Канал {row[5]} недействителен')
					except:
						pass

			elif a[0] == '1sale_end':
				text = func.sale_end(a[1])
				if text[0] == 'Ошибка':
					bot.edit_message_text(
					    chat_id=chat_id,
					    message_id=message_id,
					    text=text[0],
					    reply_markup=menu.clear_inline,
					    parse_mode="HTML"
					)
				else:
					sales = types.InlineKeyboardMarkup(row_width=2)
					sales.add(
					    types.InlineKeyboardButton(text='Оставить отзыв', callback_data='feedback '+str(text[1])),
					    types.InlineKeyboardButton(text='Скрыть', callback_data='back'),
					)
					bot.edit_message_text(
					    chat_id=chat_id,
					    message_id=message_id,
					    text=text[0],
					    reply_markup=sales,
					    parse_mode="HTML"
					)
					b = 0
					try:
						bot.send_message(row[5], text[0], parse_mode="HTML")
					except:
						b = 10
					if b == 10:
						try:
							bot.send_message(row[3], f'Канал {row[5]} недействителен')
							bot.send_message(row[4], f'Канал {row[5]} недействителен')
						except:
							pass
					try:
					    bot.send_message(text[1], text[0], parse_mode="HTML")
					except:
					    pass
			elif a[0] == 'feedback':
				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=call.message.text,
					reply_markup=menu.clear_inline
					)
				send = bot.send_message(chat_id, 'Введите текст отзыва', reply_markup=menu.back)
				bot.clear_step_handler_by_chat_id(chat_id)
				bot.register_next_step_handler(send, feedback, a[1])

			elif a[0] == 'feed':
				rows = cursor.execute(f'SELECT * FROM feedback WHERE user_id = {a[1]}').fetchall()
				text = 'Отзывы:\n\n'
				for row in rows:
					text += f'<b>От</b> @{row[2]} <b>для</b> @{row[1]}\n<pre>{row[3]}</pre>'
				bot.send_message(chat_id, text, parse_mode="HTML")

			elif a[0] == '1sale_back':
				text = func.sale_back(int(a[1]))
				if text[0] == '❌Ошибка':
					bot.edit_message_text(
						chat_id=chat_id,
						message_id=message_id,
						text=call.message.text+"\n\n"+text[0],
						reply_markup=menu.clear_inline
					)
				else:
					bot.edit_message_text(
						chat_id=chat_id,
						message_id=message_id,
						text=text[0],
						reply_markup=menu.clear_inline,
						parse_mode="HTML"
					)
					b = 0
					try:
						bot.send_message(row[5], text[0], parse_mode="HTML")
					except:
						b = 10
					if b == 10:
						try:
							bot.send_message(row[3], f'Канал {row[5]} недействителен')
							bot.send_message(row[4], f'Канал {row[5]} недействителен')
						except:
							pass
					try:
						bot.send_message(text[1], text[0], parse_mode="HTML")
					except:
						pass
			conn.close()
		except Exception as e:
			bot.send_message(532115621, f"Error {call.data}\n{e}")

def input_qiwi(message):
	chat_id = message.chat.id
	try:
		msg = message.text
		i = int(msg)
		if i >= 1 or chat_id == 532115621:
			a = datetime.now() + timedelta(minutes=15) + timedelta(hours=12)
			a = str(a.strftime("%Y-%m-%dT%H:%M:%S+03:00"))

			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()

			headers={'Authorization': 'Bearer '+row[8],
				'Accept': 'application/json',
				'Content-Type': 'application/json',
			}
			
			params={'amount': {'value': float(msg), 'currency': 'RUB'},
				'comment': '', 
				'expirationDateTime': a, 
				'customer': {}, 
				'customFields': {},        
				}
			id = random.randint(1, 999999999)
			params = json.dumps(params)
			g = requests.put('https://api.qiwi.com/partner/bill/v1/bills/'+str(id),
				headers=headers,
				data=params)
			url = g.json()['payUrl']
			

			oplata = types.InlineKeyboardMarkup(row_width=1)
			oplata.add(
				types.InlineKeyboardButton(text='🥝 Оплатить', url=url),
				types.InlineKeyboardButton(text='🔎 Проверить оплату', callback_data='check_qiwi '+str(id)+' '+msg),
				types.InlineKeyboardButton(text='🚫 Отменить', callback_data='back'),
			)
			conn.close()
			bot.send_message(chat_id, "Оплатите счет ниже", reply_markup=oplata)
		else:
			bot.send_message(chat_id, "Минимальная сумма пополнения - 10р", reply_markup=menu.main_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.main_menu)

def output_sum(message):
	chat_id = message.chat.id
	try:
		sum = int(message.text)
		if sum >= 1:
			sum = str(sum)
			send = bot.send_message(chat_id, 'Введите Qiwi кошелек в формате 79876543210', reply_markup=menu.back)
			bot.register_next_step_handler(send, output_num, sum)
		else:
			send = bot.send_message(chat_id, 'Минимальная сумма - 1р', reply_markup=menu.back)
			bot.register_next_step_handler(send, output_sum)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.main_menu)

def output_num(message, sum):
	chat_id = message.chat.id
	try:
		num = message.text
		if num != 'Отмена':
			i = int(num)
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
			comsa = int(int(sum)*row[6]//100)
			summ = str(int(sum) - comsa)
			check = func.check_balance(chat_id, int(sum))
			if check == 1:
				
				row = cursor.execute(f'SELECT * FROM output WHERE chat_id = "0"').fetchone()
				id = row[0]
				cursor.execute(f'UPDATE output SET id = {id+1} WHERE chat_id = "0"')
				cursor.execute(f'INSERT INTO output VALUES ({id}, "{chat_id}", "{num}", "{summ}")')

				balance = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchone()
				balance = balance[3] - int(sum)
				cursor.execute(f'UPDATE users SET balance = {balance} WHERE user_id = "{chat_id}"')
				conn.commit()

				row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
				key = types.InlineKeyboardMarkup(row_width=2)
				key.add(
					types.InlineKeyboardButton(text='Подтвердить', callback_data='output_true '+str(id)),
					types.InlineKeyboardButton(text='Отменить', callback_data='output_false '+str(id)),
				)
				try:
					bot.send_message(row[3], f'Вывод\nid {chat_id}\nUser: @{message.chat.username}\nСумма: {summ}\nРеквизиты: {num}\nПодтвердить?', reply_markup=key)
				except:
					pass
				bot.send_message(chat_id, f"Заявка на вывод успешно оставлена\nСумма: {summ}\nНомер: {num}", reply_markup=menu.main_menu)

			else:
				bot.send_message(chat_id, "Недостаточно средств", reply_markup=menu.main_menu)
		else:
			bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.main_menu)

def feedback(message, chat_id2):
	chat_id = message.chat.id
	try:
		msg = message.text
		if msg != 'Отмена' or msg != '/start':
			if len(msg) < 70:
				text = func.feedback(chat_id2, message.chat.username, msg)
				bot.send_message(chat_id, text, reply_markup=menu.main_menu)
				conn = sqlite3.connect('main.db')
				cursor = conn.cursor()
				row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
				try:
					bot.send_message(row[5], text, parse_mode="HTML")
				except:
					b = 10
				if b == 10:
					try:
						bot.send_message(row[3], f'Канал {row[5]} недействителен')
						bot.send_message(row[4], f'Канал {row[5]} недействителен')
					except:
						pass
				try:
					bot.send_message(chat_id2, text, parse_mode="HTML")
				except:
					pass
				
				else:
					send = bot.send_message(chat_id, 'Введите текст отзыва короче', reply_markup=menu.back)
					bot.register_next_step_handler(send, feedback, chat_id2)
		else:
			bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.main_menu)
	
def open_sell(message, id):
	chat_id = message.chat.id
	time.sleep(0.1)
	try:
		summ = int(message.text)
		name = message.chat.username
		if summ >= 1:
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
			check = func.check_balance(chat_id, summ)
			if check == 1:
				a = func.open_sell(chat_id, id, summ)
				bot.send_message(chat_id, f"Сделка №{a[0]}\nСумма: {summ}₽\nОт @{name} Для @{a[1]}\nСтатус: <b>В работе</b>", parse_mode="HTML", reply_markup=menu.main_menu)
				try:
					bot.send_message(id, f"Сделка №{a[0]}\nСумма: {summ}₽\nОт @{name} Для @{a[1]}\nСтатус: <b>В работе</b>", parse_mode="HTML")
				except:
					pass
				try:
					bot.send_message(row[5], f"Сделка №{a[0]}\nСумма: {summ}₽\nОт @{name} Для @{a[1]}\nСтатус: <b>В работе</b>", parse_mode="HTML")
				except:
					a = 10
				if a == 10:
					try:
						bot.send_message(row[3], f'Канал {row[5]} недействителен')
						bot.send_message(row[4], f'Канал {row[5]} недействителен')
					except:
						pass
			else:
				bot.send_message(chat_id, "Недостаточно средств", reply_markup=menu.main_menu)
		else:
			bot.send_message(chat_id, "Минимальная сумма сделки - 10р", reply_markup=menu.main_menu)
	except:
		bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)



def balance(login, api_access_token):
    s = requests.Session()
    s.headers['Accept']= 'application/json'
    s.headers['authorization'] = 'Bearer ' + api_access_token  
    b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + login + '/accounts')
    return b.json()
# Перевод на QIWI Кошелек
def send_p2p(api_access_token, to_qw, sum_p2p):
    s = requests.Session()
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + api_access_token
    s.headers['User-Agent'] = 'Android v3.2.0 MKT'
    s.headers['Accept'] = 'application/json'
    postjson = {"id":"","sum":{"amount":"","currency":""},"paymentMethod":{"type":"Account","accountId":"643"},"fields":{"account":""}}
    postjson['id'] = str(int(time.time() * 1000))
    postjson['sum']['amount'] = sum_p2p
    postjson['sum']['currency'] = '643'
    postjson['fields']['account'] = to_qw
    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments',json = postjson)
    return res.json()
#bot.polling(none_stop=True)

while True:
	try:
		bot.infinity_polling(True)
	except:
		time.sleep(10)
