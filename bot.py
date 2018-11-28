import logging

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from py_translator import Translator
from py_translator import LANGUAGES
import commands
import settings
import model

updater = Updater(token=settings.BOT_TOKEN)
dispatcher = updater.dispatcher
storage = model.Storage(settings.HOST, settings.DB)
command_handler = commands.Command()


def start(bot, update):
    command_handler.command_start(bot, update)


def respond(bot, update):
    command_handler.command_respond(bot, update)


def join(bot, update):
    command_handler.command_join(bot, update)

def lang(bot, update, args):
    command_handler.command_lang(bot, update, args)


dispatcher.add_handler(CommandHandler('join', join))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('lang', lang,pass_args=True))
dispatcher.add_handler(MessageHandler(Filters.text, respond))

# logger.info("Start polling")
updater.start_polling()