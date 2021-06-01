import telebot
from telebot import types

admin = telebot.types.ReplyKeyboardMarkup(True)
admin.row('Статистика','Рассылка')
admin.row('Настройки','Пользователи')
admin.row('Арбитражи','Cделки')
admin.row('Автопостинг','Выплаты','Gift')



main = telebot.types.ReplyKeyboardMarkup(True)
main.row('🔍 Открыть сделку','💻 Мой профиль','🤝 Мои сделки')
main.row('📖 F.A.Q','🎲 Игры')
main.row('🚫 SCAM LIST','🔰 Интеграция в чат')

otmena = telebot.types.ReplyKeyboardMarkup(True)
otmena.row('Отмена')

otziv = telebot.types.ReplyKeyboardMarkup(True)
otziv.row('Да', 'Нет')
