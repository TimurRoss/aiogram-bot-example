from typing import Union

from aiogram.filters import BaseFilter
from aiogram import types
import logging


class ChatTypeFilter(BaseFilter):  # [1]
    def __init__(self, chat_type: Union[str, list]): # [2]
        self.chat_type = chat_type

    async def __call__(self, message: types.Message) -> bool:  # [3]
        logging.debug(f'FILTER START (ChatTypeFilter)')
        if isinstance(self.chat_type, str):
            result = message.chat.type == self.chat_type
        else:
            result = message.chat.type in self.chat_type
        logging.debug(f'FILTER FINISHED with - {result} - (ChatTypeFilter)')
        return result

class ChatTypeFilterCallBack(BaseFilter):  # [1]
    def __init__(self, chat_type: Union[str, list]): # [2]
        self.chat_type = chat_type

    async def __call__(self, callback: types.CallbackQuery) -> bool:  # [3]
        if isinstance(self.chat_type, str):
            return callback.message.chat.type == self.chat_type
        else:
            return callback.message.chat.type in self.chat_type