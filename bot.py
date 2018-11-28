import logging

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from py_translator import Translator
from py_translator import LANGUAGES
import settings

chats=['650305195;en','596881935;ar','575565672;iw']
logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=settings.BOT_TOKEN)
dispatcher = updater.dispatcher

def start(bot, update):
    chat_id = update.message.chat_id
    logger.info(f"> Start chat #{chat_id}")
    bot.send_message(chat_id=chat_id, text="HELLO")


def respond(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")

    # bot.send_message(chat_id=update.message.chat_id, text=response)
    for c in chats:
        if not (int(c.split(';')[0]) == chat_id):
            response = Translator().translate(text, dest=c.split(';')[1]).text
            print (f"c = {type(c)}")
            print (f"c1 = {type(chat_id)}")
            bot.send_message(chat_id=c, text= update.message['from_user']['first_name'] +" : " +response)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)

logger.info("Start polling")
updater.start_polling()
