import os
import telebot
import logging
from flask import Flask, request
from telebot import types

token = os.environ['TOKEN']
bot = telebot.TeleBot(token)
symb = '+'
cue = os.environ['CUE']

@bot.message_handler(content_types=['text'])
def echo_message(message):
    if symb in message.text:
        if message.from_user.username == 'Artem_Barsov' or message.from_user.id == 121442647:
            bot.reply_to(message, symb)
        else:
            bot.reply_to(message, cue)

if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)
    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://fcking-boar.herokuapp.com/bot")
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    bot.remove_webhook()
    bot.polling(none_stop=True)
