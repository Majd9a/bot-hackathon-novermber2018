import telegram
from py_translator import Translator, LANGUAGES
from messages import messages
import model
import settings
import logging


class Command:

    def __init__(self):
        self.storage = model.Storage(settings.HOST, settings.DB)
        logging.basicConfig(
            format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

    def command_start(self, bot, update):
        chat_id = update.message.chat_id
        first_name = update.message['from_user']['first_name']
        last_name = update.message['from_user']['last_name']
        print(update.message)

        language = 'en'
        self.logger.info(f"> Start chat #{chat_id}")
        bot.send_message(chat_id=chat_id, text="HELLO")
        print("check here ", chat_id)
        self.storage.add_user(chat_id, language, first_name, last_name)

        kb = [[telegram.KeyboardButton("/join")]]
        kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Welcome!",
                         reply_markup=kb_markup)

    # def command_create(self,bot, update,args):
    #     ## put to data base
    #     pass

    # def command_user_details(self,bot, update, args):
    #     user_id = update.message.chat_id
    #     lang = args[0]
    #     #update for user the room id
    def command_lang(self, bot, update, args):
        chat_id = update.message.chat_id
        first_name = update.message['from_user']['first_name']
        last_name = update.message['from_user']['last_name']
        language = args[0]
        self.storage.add_user(chat_id, language, first_name, last_name)

    def command_join(self, bot, update):
        kb = []
        langs = sorted(LANGUAGES.keys())
        for key in langs:
            kb.append([telegram.KeyboardButton("/lang " + key)])

        kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Welcome!",
                         reply_markup=kb_markup)

        # room_id = int(args[0])
        # user_id = update.message.chat_id
        # first_name = update.message['chat']['first_name']
        # last_name = update.message['chat']['last_name']
        # ### send  username details to database(chat id) for the room and defult lang eng
        # msg = messages(f"{first_name} {last_name} joined ", bot)
        # msg.send_to(user_id)
        # msg.broadcast(room_id)

    def command_respond(self, bot, update):
        user_id = update.message.chat_id
        text = update.message.text
        ##get the room that user uses
        self.logger.info(f"= Got on chat #{user_id}: {text!r}")
        for i in self.storage.users.find():
            userId = int(i['_id'])
            if not (userId == user_id):
                ## translate to user lang
                response = Translator().translate(text, dest=i['language']).text
                ## send to users
                msg = messages(update.message['from_user']['first_name'] + " : " + response, bot)
                msg.send_to(userId)
