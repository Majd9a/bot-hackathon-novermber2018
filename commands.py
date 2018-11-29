import telegram
from py_translator import Translator, LANGUAGES
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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

        language = 'en'
        self.logger.info(f"> Start chat #{chat_id}")

        if not self.storage.users.find_one({"_id": chat_id}):
            self.storage.add_user(chat_id, language, first_name, last_name)

        kb = [[telegram.KeyboardButton("/change_lang")]]
        kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id,
                         text=f"Hello {first_name}, and welcome to the multi language bot!",
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
        language = args[0]
        self.storage.users.update_one({"_id": chat_id},
                                      {"$set": {'language': language}},
                                      upsert=True)

    def command_memebers(self, bot, update):
        members = self.storage.users.find()  # return list of string
        user_id = update.message.chat_id
        curr_room_id = self.storage.users.find_one({"_id": user_id})['room_id']
        print(members)

        keyboard = []
        for j, i in enumerate(members):
            if (i['room_id'] == curr_room_id):
                keyboard.append([InlineKeyboardButton(i['first_name'] + " " + i['last_name'], callback_data=f"{j}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f'Members of {curr_room_id}:', reply_markup=reply_markup)

    def command_join(self, bot, update, args):
        room_id = args[0]
        chat_id = update.message.chat_id
        prev_room_id = self.storage.users.find_one({"_id": chat_id})['room_id']
        print(self.storage.users.find_one({"_id": chat_id})['room_id'])

        if self.storage.rooms.find_one({"_id": room_id}):
            self.storage.users.update_one({"_id": chat_id},
                                          {"$set": {'room_id': room_id}},
                                          upsert=True)
            msg = messages(f"You have just joined {room_id}, ENJOY!", bot)
            msg.send_to(update.message.chat_id)

            first_name = update.message['from_user']['first_name']
            last_name = update.message['from_user']['last_name']

            msgBroadcast = messages(f"{first_name} {last_name} just joined {room_id}!", bot)
            msgBroadcast.broadcast(room_id)

            msgBroadcast = messages(f"{first_name} {last_name} just left this room!", bot)
            msgBroadcast.broadcast(prev_room_id)
        else:
            msg = messages(f"Room {room_id} does not exist!", bot)
            msg.send_to(update.message.chat_id)

    def command_create(self, bot, update, args):
        room_id = args[0]
        if not self.storage.rooms.find_one({"_id": room_id}):
            self.storage.rooms.update_one({"_id": room_id},
                                          {"$set": {"created_by": update.message.chat_id}},
                                          upsert=True)
            msg = messages(f"Room name {room_id} has been successfully created", bot)
            msg.send_to(update.message.chat_id)
        else:
            msg = messages(f"Room name {room_id} already exists ", bot)
            msg.send_to(update.message.chat_id)

    def command_change_lang(self, bot, update):
        kb = []
        langs = sorted(LANGUAGES.keys())
        for key in langs:
            kb.append([telegram.KeyboardButton("/lang " + key)])

        kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Choose a language please",
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
        curr_room_id = self.storage.users.find_one({"_id": user_id})['room_id']
        print(curr_room_id)
        for i in self.storage.users.find():
            userId = int(i['_id'])
            if not (userId == user_id):
                if (i['room_id'] == curr_room_id):
                    ## translate to user lang
                    response = Translator().translate(text, dest=i['language']).text
                    ## send to users
                    msg = messages(update.message['from_user']['first_name'] + " : " + response, bot)
                    msg.send_to(userId)
