# - *- coding: utf- 8 - *-
# Библеотека бота
import telebot
from telebot import types

# Библеотека для извлечения токена из файла
from dotenv import load_dotenv
import os

# Библеотека класс переводчика
from game import Translation

# Библеотека игры "Висельница"
from game import Hangman

# Библеотека логирования
import logging

env_path = '../.env'
load_dotenv(dotenv_path=env_path)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

logging.info('Started')

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
bot.remove_webhook()


# Поток обработки основного меню
@bot.message_handler(commands=['start'])
def welcome(message):
    Translation.set_lang(message.from_user)
    main_menu_callback(types.CallbackQuery(None, message.from_user, "Hangman", None, message))


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, Translation.get_hangman_exp("HELP", user_id=message.from_user.id))


@bot.message_handler(commands=['playHangman'])
def handle_text(message):
    main_menu_callback(types.CallbackQuery(None, message.from_user, "Hangman", None, message))


@bot.message_handler(content_types=['text', 'photo'])
def dating_handler(message):
    print(message)


@bot.callback_query_handler(func=lambda call: True)
def main_menu_callback(call):
    if call.data == "language_ru" or call.data == "language_en":
        Translation.switch_language(call.from_user.id)
        call.data = "Hangman"
        Hangman.get_callback(call, bot, Translation.get_player_language(call.from_user.id))
    elif call.data in Hangman.call_list:
        Hangman.get_callback(call, bot, Translation.get_player_language(call.from_user.id))


if __name__ == "__main__":
    bot.polling(none_stop=True)
    logging.info('Finished')
