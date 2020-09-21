import os
import pickle
from collections import defaultdict
from copy import deepcopy
from telegram.ext import BasePersistence
import psycopg2


class MyPersistence(BasePersistence):

    def __init__(self, store_user_data=True, store_chat_data=True, store_bot_data=True):
        super().__init__(store_user_data, store_chat_data, store_bot_data)
        self.connect = psycopg2.connect(user=os.environ.get("db_login"),
                                        password=os.environ.get("db_password"),
                                        host=os.environ.get("db_host"),
                                        dbname=os.environ.get("db_name"))

        self.sql_get = "select save_data from public.bot_chat_persist where type_save = %s"
        self.sql_save = "update public.bot_chat_persist set save_data = %s where type_save = %s"
        self.save_types = ["user_data", "chat_data", "bot_data", "conversations"]
        self.user_data = None
        self.chat_data = None
        self.bot_data = None
        self.conversations = None

    def load(self):
        data = {}
        try:
            cur = self.connect.cursor()
            for save_type in self.save_types:
                cur.execute(self.sql_get, (save_type,))
                temp = cur.fetchall()[0][0]
                print(temp)
                if temp is not None:
                    data[save_type] = pickle.loads(temp)
                else:
                    data[save_type] = {}
            cur.close()
            self.user_data = defaultdict(dict, data['user_data'])
            self.chat_data = defaultdict(dict, data['chat_data'])
            # For backwards compatibility with files not containing bot data
            self.bot_data = data.get('bot_data', {})
            self.conversations = data['conversations']
        except IOError:
            self.conversations = {}
            self.user_data = defaultdict(dict)
            self.chat_data = defaultdict(dict)
            self.bot_data = {}

    def dump(self):
        data = {'conversations': self.conversations, 'user_data': self.user_data,
                'chat_data': self.chat_data, 'bot_data': self.bot_data}
        cur = self.connect.cursor()
        for save_type in self.save_types:
            cur.execute(self.sql_save, (pickle.dumps(data.get(save_type)), save_type))
        self.connect.commit()
        cur.close()

    def get_user_data(self):
        """Returns the user_data from the pickle file if it exsists or an empty defaultdict.

        Returns:
            :obj:`defaultdict`: The restored user data.
        """
        if self.user_data:
            pass
        else:
            self.load()
        return deepcopy(self.user_data)

    def get_chat_data(self):
        """Returns the chat_data from the pickle file if it exsists or an empty defaultdict.

        Returns:
            :obj:`defaultdict`: The restored chat data.
        """
        if self.chat_data:
            pass
        else:
            self.load()
        return deepcopy(self.chat_data)

    def get_bot_data(self):
        """Returns the bot_data from the pickle file if it exsists or an empty dict.

        Returns:
            :obj:`defaultdict`: The restored bot data.
        """
        if self.bot_data:
            pass
        else:
            self.load()
        return deepcopy(self.bot_data)

    def get_conversations(self, name):
        """Returns the conversations from the pickle file if it exsists or an empty defaultdict.

        Args:
            name (:obj:`str`): The handlers name.

        Returns:
            :obj:`dict`: The restored conversations for the handler.
        """
        if self.conversations:
            pass
        else:
            self.load()
        return self.conversations.get(name, {}).copy()

    def update_conversation(self, name, key, new_state):
        """Will update the conversations for the given handler and depending on :attr:`on_flush`
        save the pickle file.

        Args:
            name (:obj:`str`): The handlers name.
            key (:obj:`tuple`): The key the state is changed for.
            new_state (:obj:`tuple` | :obj:`any`): The new state for the given key.
        """
        if self.conversations.setdefault(name, {}).get(key) == new_state:
            return
        self.conversations[name][key] = new_state
        self.dump()

    def update_user_data(self, user_id, data):
        """Will update the user_data (if changed) and depending on :attr:`on_flush` save the
        pickle file.

        Args:
            user_id (:obj:`int`): The user the data might have been changed for.
            data (:obj:`dict`): The :attr:`telegram.ext.dispatcher.user_data` [user_id].
        """
        if self.user_data is None:
            self.user_data = defaultdict(dict)
        if self.user_data.get(user_id) == data:
            return
        self.user_data[user_id] = data
        self.dump()

    def update_chat_data(self, chat_id, data):
        """Will update the chat_data (if changed) and depending on :attr:`on_flush` save the
        pickle file.

        Args:
            chat_id (:obj:`int`): The chat the data might have been changed for.
            data (:obj:`dict`): The :attr:`telegram.ext.dispatcher.chat_data` [chat_id].
        """
        if self.chat_data is None:
            self.chat_data = defaultdict(dict)
        if self.chat_data.get(chat_id) == data:
            return
        self.chat_data[chat_id] = data
        self.dump()

    def update_bot_data(self, data):
        """Will update the bot_data (if changed) and depending on :attr:`on_flush` save the
        pickle file.

        Args:
            data (:obj:`dict`): The :attr:`telegram.ext.dispatcher.bot_data`.
        """
        if self.bot_data == data:
            return
        self.bot_data = data.copy()
        self.dump()

    def flush(self):
        """ Will save all data in memory to pickle file(s).
        """
        if self.user_data or self.chat_data or self.conversations:
            self.dump()
        self.connect.close()
