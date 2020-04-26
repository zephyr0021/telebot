# -*- coding: utf-8 -*-
import telebot
from telebot import types
from bs4 import BeautifulSoup as BS
import sqlite3
from requests import get
list = ['Ужасы', 'Комедия', 'Боевик', 'Драма']
bot = telebot.TeleBot('984351635:AAFRjoWJM3-ih9ODT3lHzx4PhrEqYLCpV8A')
button_horror = types.KeyboardButton('Ужасы')
button_comedy = types.KeyboardButton('Комедия')
button_drama = types.KeyboardButton('Драма')
button_action = types.KeyboardButton('Боевик')
greet_kb = types.ReplyKeyboardMarkup()
greet_kb.add(button_horror,button_comedy,button_drama,button_action)
what_to_do = ''
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if message.text == "Привет":
		bot.send_message(message.from_user.id, "Привет, выбери жанр:",reply_markup=greet_kb)
	elif message.text == "/help":
		bot.send_message(message.from_user.id, "Этот раздел находится в разработке, просто напиши боту Привет")
	elif message.text in list:
		conn = sqlite3.connect('mydatabase.sqlite')
		c = conn.cursor()
		films_of_type = c.execute("SELECT name, description, content FROM Films WHERE type = '{}'".format(message.text))
		x = films_of_type.fetchall()
		for a in x:
			bot.send_photo(message.from_user.id, get("{}".format(a[2])).content, caption= "Название фильма: {}\n\nОписание: {}".format(a[0],a[1]))
		conn.close()
bot.polling(none_stop=True, interval=0)
