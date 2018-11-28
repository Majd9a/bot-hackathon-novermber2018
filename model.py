# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
from pymongo.mongo_client import MongoClient


class Storage:
    def __init__(self, host, db):
        self.client = MongoClient(host)
        self.db = self.client.get_database(db)
        self.users = self.db.get_collection("users")
        self.logs = self.db.get_collection("logs")

        self.users.create_index("id_room", unique=True)

    def create_list_users(self, id_room):
        self.users.replace_one({'id_room': id_room}, {
            'id_room': id_room,
            'users': [],
            'logs': [],
        }, upsert=True)

    # details :id_user, first_name, last_name, language
    def add_user_to_list(self, id_room, user):
        self.lists.update_one({'id_room': id_room}, {
            '$push': {'users': user},
        })

    # logs :mesg, sender , time
    def add_user_to_list(self, id_room, msg, sender, time):
        self.lists.update_one({'id_room': id_room}, {
            '$push': {'logs': [msg, sender, time]},
        })

    def get_doc(self, id_room):
        return self.lists.find_one({'id_room': id_room})

    def count_users(self, id_room):
        doc = self.get_doc(id_room)
        return len(doc['users'])

    def get_users(self, id_room):
        doc = self.get_doc(id_room)
        return doc['users']
