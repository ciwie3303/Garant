import re
from decimal import Decimal
import time
import config
import requests
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetMessagesRequest
from telethon.tl.functions.messages import GetHistoryRequest, ReadHistoryRequest
from telethon import TelegramClient, events, sync
import telethon.sync
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import telebot
import sqlite3
import datetime
from datetime import datetime, timedelta
api_id = 988074
api_hash = 'a5ec8b7b6dbeedc2514ca7e4ba200c13'


client = TelegramClient('coma', api_id, api_hash, device_model="Iphone", system_version="6.12.0", app_version="10 P (28)")
client.start()

bot = telebot.TeleBot(config.bot_token_pay)

def btc():
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	global i
	q.execute(f"SELECT * FROM BTC_CHANGE_BOT where status != 'del' ")
	info = q.fetchall()
	for i in info:
		if i != None:
			q.execute(f"update BTC_CHANGE_BOT set status = 'del' where text = '{i[1]}'")
			connection.commit()
			client.send_message('BTC_CHANGE_BOT', f'/start {i[1][41:]}')
			time.sleep(4)
			answer = btc_check()
			if 'Вы получили' in str(answer) and 'RUB' in str(answer):
				btc_summa = re.findall('Вы\ получили\ ([0123456789\,\.]*)\ BTC', answer)
				summa_plus_balance = str(answer).split('(')[1].split(' ')[0]
				q.execute(f"update BTC_CHANGE_BOT set status = 'del' where text = '{i[1]}'")
				connection.commit()
				q.execute(f"update ugc_users set balans = balans +'{summa_plus_balance}' where id = '{i[6]}'")
				connection.commit()
				bot.send_message(i[6], f'''💎 Успешная оплата на сумму: {summa_plus_balance} RUB''')
			elif 'Упс, кажется, данный чек успел обналичить кто-то другой 😟' in str(answer):
				bot.send_message(i[6], f'''Упс, кажется, данный чек успел обналичить кто-то другой 😟''')
				pass

			else:
				pass

def btc_check():
	channel_username='BTC_CHANGE_BOT'
	channel_entity=client.get_entity(channel_username)
	posts = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
	mesages = posts.messages
	for i in mesages:
		answer = i.message
		return answer

while True:
	time.sleep(2)
	btc()

client.run_until_disconnected()