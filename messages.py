class messages:
    def __init__(self,msg,bot):
        self.msg = msg
        self.bot = bot

    def send_to(self,chat_id):
        self.bot.send_message(chat_id=chat_id, text=self.msg)
        pass

    def broadcast(self,room_id):
        # get all chats numbers from db for specific room_id
        pass