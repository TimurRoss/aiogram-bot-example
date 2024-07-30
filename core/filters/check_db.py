import logging

from core.db.mysql_connect import mysql

from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram import types


class CheckDbFilter(BaseFilter):  # [1]
    def __init__(self,table,source='Source is none', **kwargs): # [2]
        self.parametrs = kwargs
        self.table=table
        self.source= source

    async def __call__(self, message: Message) -> bool:  # [3]
        logging.debug(f'FILTER START (CheckDbFilter)')
        logging.debug(f'------ source: {self.source}')
        logging.debug(f"------ arg: {self.parametrs.values()} {self.parametrs.keys()} {message}")
        arg = dict()
        result = None
        for key,value in self.parametrs.items():
            if value=="user_id":
                if message.from_user.id is None:
                    result = False
                else:
                    arg[key]=message.from_user.id
            elif value=="chat_id":
                arg[key]=message.chat.id
            elif value=="user_login":
                if message.from_user is None:
                    result = False
                else:
                    if message.from_user.username is None:
                        result = False
                    else:
                        arg[key] = '@'+message.from_user.username
            elif value=="message_id":
                arg[key] = message.id
            elif value=="message_thread_id":
                arg[key] = message.message_thread_id
            elif value=='null':
                arg[key] = None
            elif value=='not null':
                arg[key] = 'NOT NULL'
            else:
                result = False
        if result is None:
            result = mysql.check(table=self.table,
                            __arg=arg)

        logging.debug(f'FILTER FINISHED with - {result} - (CheckDbFilter)')
        return result

class CheckDbFilterCallback(BaseFilter):  # [1]
    def __init__(self,table, **kwargs): # [2]
        self.parametrs = kwargs
        self.table=table

    async def __call__(self, callback: types.CallbackQuery) -> bool:  # [3]

        arg = dict()
        for key, value in self.parametrs.items():
            if value == "user_id":
                if callback.message.from_user is None:
                    pass
                else:
                    arg[key] = callback.message.from_user.id
            elif value == "chat_id":
                arg[key] = callback.message.chat.id
            elif value == "user_login":
                if callback.message.from_user is None:
                    pass
                else:
                    arg[key] = '@' + callback.message.from_user.username
            elif value=="message_id":
                arg[key] = callback.message.id
            elif value == 'null':
                arg[key] = None
            elif value=='not null':
                arg[key] = 'NOT NULL'
            else:
                return False

        result = mysql.check(table=self.table,
                             __arg=arg)
        logging.debug(f"(filter) {result} {self.parametrs.values()} {self.parametrs.keys()} {callback}")
        return result

class CheckDbFilterEmoji(BaseFilter):  # [1]
    def __init__(self,table, **kwargs): # [2]
        self.parametrs = kwargs
        self.table=table

    async def __call__(self, reaction: types.MessageReactionUpdated) -> bool:  # [3]
        arg = dict()
        for key, value in self.parametrs.items():
            if value == "user_id":
                if reaction.user is None:
                    pass
                else:
                    arg[key] = reaction.user.id
            elif value == "chat_id":
                logging.debug(reaction.chat.id)
                arg[key] = reaction.chat.id
            elif value == "user_login":
                if reaction.user.username is None:
                    pass
                else:
                    arg[key] = '@' + reaction.user.username
            elif value=="message_id":
                arg[key] = reaction.message_id
            elif value == 'null':
                arg[key] = None
            elif value == 'not null':
                arg[key] = 'NOT NULL'
            else:
                return False

        result = mysql.check(table=self.table,
                             __arg=arg)
        # logging.debug(f"(filter) {result} {self.parametrs.values()} {self.parametrs.keys()} {reaction}")
        return result
