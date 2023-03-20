import pymongo
from datetime import datetime


class ChatAppDB:
    def __init__(self, uri):
        client = pymongo.MongoClient(uri)
        self.db = client.imsgs

    def get_user_conversation(self, sender_name):
        conversation = self.db.conversations.find_one({"senderName": sender_name})
        return conversation

    def get_last_8_messages(self, sender_name, topic):
        conversation = self.get_user_conversation(sender_name)
        if not conversation or topic not in conversation['topics']:
            return []

        messages = conversation['topics'][topic]['messages']
        return messages[-8:]

    def create_conversation(self, sender_name):
        conversation = {
            "senderName": sender_name,
            "topics": {}
        }
        result = self.db.conversations.insert_one(conversation)
        return str(result.inserted_id)

    def add_message(self, sender_name, topic, role, msg):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = {
            "role": role,
            "msg": msg,
            "time": now
        }
        result = self.db.conversations.update_one(
            {"senderName": sender_name},
            {"$push": {"topics." + topic + ".messages": message}}
        )
        return result.modified_count

    def update_message(self, sender_name, topic, index, new_msg):
        result = self.db.conversations.update_one(
            {"senderName": sender_name},
            {"$set": {"topics." + topic + ".messages." + str(index) + ".msg": new_msg}}
        )
        return result.modified_count

    def delete_message(self, sender_name, topic, index):
        result = self.db.conversations.update_one(
            {"senderName": sender_name},
            {"$pull": {"topics." + topic + ".messages": {"$gte": {"index": index}}}}
        )
        return result.modified_count
