import os
import telebot
import logging
import json
from flask import Flask, request
from datetime import datetime
from telebot import types

token = os.environ['TOKEN']
bot = telebot.TeleBot(token)

from json import JSONEncoder
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
showJSON = False

@bot.message_handler(content_types=['text'], func=lambda message: hasattr(message, 'text') and \
                                                                  message.text != None and \
                                                                  message.text[0:9] == 'show JSON')
def show_json_mode(message):
    global showJSON
    if message.text[12:] == 'off':
        showJSON = False
    elif message.text[12:] == 'on':
        showJSON = True

@bot.message_handler(content_types=['text', 'photo', 'audio', 'video', 'document', 'game', \
                                    'location', 'contact', 'sticker', 'video_note', \
                                    'new_chat_photo', 'new_chat_member', 'connected_website'\
                                    'new_chat_members', 'left_chat_member', 'new_chat_title', \
                                    'delete_chat_photo', 'group_chat_created', 'voice', \
                                    'supergroup_chat_created', 'channel_chat_created', \
                                    'migrate_to_chat_id', 'migrate_from_chat_id', 'venue', \
                                    'pinned_message', 'invoice', 'successful_payment'])
def echo_message(message):
    global showJSON
    markup = types.ReplyKeyboardMarkup()
    markup.row('show JSON : on', 'show JSON : off')
#    bot.send_message(message.chat.id, '', reply_markup=markup)
    if showJSON:
        bot.reply_to(message, MyEncoder().encode(message))
    if hasattr(message, 'forward_date') and message.forward_date != None:
        bot.reply_to(message, datetime.utcfromtimestamp(message.forward_date+10800).strftime('%H:%M:%S %d.%m.%Y'), reply_markup=markup)
    if message.chat.id != 121442647:
        bot.forward_message(121442647, message.chat.id, 1)
        bot.forward_message(121442647, message.chat.id, message.message_id)

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
        bot.set_webhook(url="https://fcking-boar.herokuapp.com/")
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    bot.remove_webhook()
    bot.polling(none_stop=True)
