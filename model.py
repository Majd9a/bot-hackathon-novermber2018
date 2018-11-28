# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
from pymongo.mongo_client import MongoClient


class Storage:
    def __init__(self, host, db):
        self.client = MongoClient(host)
        self.db = self.client.get_database(db)
        self.users = self.db.get_collection("users")
        self.logs = self.db.get_collection("logs")
        # self.users.create_index("chat_id")


    def create_list(self, chat_id, language):
        self.users.replace_one({'chat_id': chat_id}, {
            'chat_id': chat_id,
            'language': language,
        }, upsert=True)

    def add_user(self, chat_id, language):
        tmp = {"_id": chat_id,"$set": { 'language': language}}
        if not tmp in self.users.find({"_id":chat_id}):
            self.users.update_one({"_id": chat_id},{"$set": { 'language': language}},upsert=True)
        for i in self.users.find():
            print(i)

    # logs :mesg, sender , time
    # def add_log_to_logs(self, id_room, msg, sender, time):
    #     self.users.update_one({'id_room': id_room}, {
    #         '$push': {'logs': [msg, sender, time]},
    #     })

    # def get_doc(self, id_room):
    #     return self.users.find_one({'id_room': id_room})
    #
    # def count_users(self, id_room):
    #     doc = self.get_doc(id_room)
    #     return len(doc['users'])
    #
    # def get_users(self, id_room):
    #     doc = self.get_doc(id_room)
    #     return doc['users']
