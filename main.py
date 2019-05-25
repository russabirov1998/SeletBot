from telebot import TeleBot
import telegram, telebot

from queries.applications import ApplicationsView
from queries.projects import ProjectsView
from queries.camps import CampsView

from utils import list_of_links, camp_detail
from constants import CAMPS_KEYWORDS_NAMES
import constants

token = open('tgtoken.txt', 'r').readline().strip()
bot = TeleBot(token)


def init_keyboard():
    camps_button = telegram.KeyboardButton('Лагеря')
    apps_button = telegram.KeyboardButton('Заявки')
    projects_button = telegram.KeyboardButton('Проекты')
    telegram.ReplyKeyboardMarkup([camps_button, apps_button, projects_button])


class Handler:
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Лагеря')
    user_markup.row('Заявки')
    user_markup.row('Проекты')
    user_markup.row('🍚', '👍', '❤')
    
    @staticmethod
    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, constants.START_MESSAGE, parse_mode=telegram.ParseMode.MARKDOWN,
                         reply_markup=Handler.user_markup)

    @staticmethod
    @bot.message_handler(commands=['help'])
    def help_message(message):
        bot.send_message(message.chat.id, constants.HELP_MESSAGE, parse_mode=telegram.ParseMode.MARKDOWN,
                         reply_markup=Handler.user_markup)

    @staticmethod
    @bot.message_handler(content_types=['text'])
    def text_messages(message):
        text = message.text.lower()
        disable_web_page_preview = True
        user_id = message.chat.id

        if text in constants.BON_APPETITE_KEYWORDS:
            bot.send_sticker(user_id, 'CAADAgADTAgAAnLvWgUxEsiriE91rAI')
            return
        elif text in constants.COOL_KEYWORDS:
            bot.send_sticker(user_id, 'CAADAgADSggAAnLvWgWPSApReQJ-cQI')
            return
        elif text in constants.LOVE_KEYWORDS:
            bot.send_sticker(user_id, 'CAADAgADSAgAAnLvWgUxx7_RczuKiwI')
            return
        elif text in CAMPS_KEYWORDS_NAMES:
            res = camp_detail(CAMPS_KEYWORDS_NAMES[text])
        elif text in constants.APPLICATIONS_KEYWORDS:
            res = list_of_links(ApplicationsView.list())
        elif text in constants.CAMPS_KEYWORDS:
            res = list_of_links(CampsView.list())
        elif text in constants.PROJECTS_KEYWORDS:
            res = list_of_links(ProjectsView.list())
        else:
            res = '_Я тебя не понимаю_'

        bot.send_message(user_id, res, parse_mode=telegram.ParseMode.MARKDOWN,
                         disable_web_page_preview=disable_web_page_preview,
                         reply_markup=Handler.user_markup)

    @staticmethod
    @bot.message_handler(content_types=['audio', 'video', 'document', 'location', 'contact', 'sticker'])
    def unsupported_messages(message):
        res = f'_Я не умею отвечать на сообщения такого типа: {message.content_type}_'
        bot.send_message(message.from_user.id, res, parse_mode=telegram.ParseMode.MARKDOWN)


init_keyboard()
bot.polling(none_stop=True, interval=0)
