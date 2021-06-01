from telebot import types


main_menu = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
main_menu.add('🔍 Найти user', '🤝 Мои сделки', '💻Мой профиль', '💬 Помощь')

admin_menu = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
admin_menu.add('Кол-во юзеров', 'Общий баланс', 'Рассылка', 'Изменить баланс', 'Оплата', 'Админы', 'Канал', 'Описание', 'Комиссия', 'Статус')
admin_menu.row('Вернуться в главное меню')

profile_menu = types.InlineKeyboardMarkup(row_width=2)
profile_menu.add(
	types.InlineKeyboardButton(text='Пополнить', callback_data='input'),
	types.InlineKeyboardButton(text='Вывод', callback_data='output'),
)

input_menu = types.InlineKeyboardMarkup(row_width=2)
input_menu.add(
	types.InlineKeyboardButton(text='Qiwi', callback_data='input_qiwi'),
)

update_name = types.InlineKeyboardMarkup(row_width=2)
update_name.add(
	types.InlineKeyboardButton(text='Есть вопрос?', url='https://t.me/LEO_SUP'),
	types.InlineKeyboardButton(text='Наш чат услуг', url='https://t.me/joinchat/TacAWBr2AE_0nWHEGibckA'),
	types.InlineKeyboardButton(text='💡Как пользоваться ботом?', callback_data='how'),

)

qiwi_menu = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
qiwi_menu.add('Токен', 'Номер', 'Карта', 'Баланс', 'Токен p2p', 'Api btc', 'Api secret btc')
qiwi_menu.add('Назад')

one_two = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
one_two.add('Первый', 'Второй', 'Отмена')

back = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
back.add('Отмена')

clear_inline = types.InlineKeyboardMarkup(row_width=2)




