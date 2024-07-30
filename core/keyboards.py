from aiogram import types

from core import tools


# ------Keyboards for admin panel----
class AdminKeyboards:
    @staticmethod
    def cmd_start():
        buttons = [
            [types.InlineKeyboardButton(text="В главное меню", callback_data='main_menu')]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
    @staticmethod
    def main_menu():
        buttons = [
            [types.InlineKeyboardButton(text="Список сотрудников", callback_data='workers_page_start')],
            [types.InlineKeyboardButton(text="Список чатов поставщиков", callback_data='providers_page_start')],
            [types.InlineKeyboardButton(text="Получить LOG файл", callback_data='send_log')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def page_list_workers_empty():
        buttons = [
            [types.InlineKeyboardButton(text="Добавить сотрудника(-ов)", callback_data='add_workers')],
            [types.InlineKeyboardButton(text="Назад", callback_data='main_menu')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def page_list_workers(page, max_page, count,list_workers,list_id):

        buttons = []

        for i in range(0, len(list_workers), 2):
            l = []
            for j in range(2):
                if i + j == len(list_workers):
                    break
                l.append(
                    types.InlineKeyboardButton(text=f'{list_workers[i + j][0]}',
                                               callback_data="worker_local_id_" + str(list_id[i + j])))
            buttons.append(l)

        if 0<=count and count<=5:
            pass
        else:
            if page == 1:
                buttons.append([types.InlineKeyboardButton(text="> Следующая >", callback_data='workers_page_next')])
            elif page == max_page:
                buttons.append([types.InlineKeyboardButton(text="< Предыдущая <", callback_data='workers_page_last')])
            else:
                buttons.append([types.InlineKeyboardButton(text="< Предыдущая <", callback_data='workers_page_last'),
                                types.InlineKeyboardButton(text="> Следующая >", callback_data='workers_page_next')])
        buttons.append([types.InlineKeyboardButton(text="Добавить", callback_data='add_workers'),
                        types.InlineKeyboardButton(text="Удалить", callback_data='delete_workers')])
        buttons.append([types.InlineKeyboardButton(text="Сортировать", callback_data='choice_worker_sort')])
        buttons.append([types.InlineKeyboardButton(text="В главное меню", callback_data='main_menu')])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def add_workers_complete():
        buttons = [
            [types.InlineKeyboardButton(text="Назад", callback_data='workers_page_start')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def add_workers_not_complete():
        buttons = [
            [types.InlineKeyboardButton(text="Назад", callback_data='workers_page_start')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def delete_workers_complete():
        buttons = [
            [types.InlineKeyboardButton(text="Назад", callback_data='workers_page_start')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def delete_workers_not_complete():
        buttons = [
            [types.InlineKeyboardButton(text="Назад", callback_data='workers_page_start')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def page_list_providers_empty():
        buttons = [
            [types.InlineKeyboardButton(text="Добавить чат поставщика(-ов)", callback_data='add_providers')],
            [types.InlineKeyboardButton(text="Назад", callback_data='main_menu')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def page_list_providers(page, max_page, count):

        buttons = []
        if 0 <= count and count <= 5:
            pass
        else:
            if page == 1:
                buttons.append([types.InlineKeyboardButton(text="> Следующая >", callback_data='providers_page_next')])
            elif page == max_page:
                buttons.append([types.InlineKeyboardButton(text="< Предыдущая <", callback_data='providers_page_last')])
            else:
                buttons.append([types.InlineKeyboardButton(text="< Предыдущая <", callback_data='providers_page_last'),
                                types.InlineKeyboardButton(text="> Следующая >", callback_data='providers_page_next')])
        buttons.append([types.InlineKeyboardButton(text="Добавить", callback_data='add_providers'),
                        types.InlineKeyboardButton(text="Удалить", callback_data='delete_providers')])
        buttons.append([types.InlineKeyboardButton(text="В главное меню", callback_data='main_menu')])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def add_providers_complete():
        buttons = [
            [types.InlineKeyboardButton(text="Назад", callback_data='providers_page_start')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def add_providers_not_complete():
        buttons = [
            [types.InlineKeyboardButton(text="Назад", callback_data='providers_page_start')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def delete_providers_complete():
        buttons = [
            [types.InlineKeyboardButton(text="Назад", callback_data='providers_page_start')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def delete_providers_not_complete():
        buttons = [
            [types.InlineKeyboardButton(text="Назад", callback_data='providers_page_start')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def worker_statistics():
        buttons = [
            [types.InlineKeyboardButton(text="Назад", callback_data='workers_page_start')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    @staticmethod
    def choice_worker_sort_complete():
        buttons = [
            [types.InlineKeyboardButton(text="Назад", callback_data='workers_page_start')],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard


    @staticmethod
    def choice_worker_sort():
        buttons = [
            [types.InlineKeyboardButton(text="Кол-во обработок (1 день)",
                                        callback_data='choice_worker_sort_'+'count_in_day')],
            [types.InlineKeyboardButton(text="Кол-во обработок (1 неделя)",
                                        callback_data='choice_worker_sort_' + 'count_in_week')],
            [types.InlineKeyboardButton(text="Кол-во обработок (1 месяц)",
                                        callback_data='choice_worker_sort_' + 'count_in_month')],
            [types.InlineKeyboardButton(text="Кол-во обработок (прошлый месяц)",
                                        callback_data='choice_worker_sort_' + 'count_in_last_month')],
            [types.InlineKeyboardButton(text="Среднее время обработок (1 день)",
                                        callback_data='choice_worker_sort_' + 'sum_time_in_day')],
            [types.InlineKeyboardButton(text="Среднее время обработок (1 неделя)",
                                        callback_data='choice_worker_sort_' + 'sum_time_in_week')],
            [types.InlineKeyboardButton(text="Среднее время обработок (1 месяц)",
                                        callback_data='choice_worker_sort_' + 'sum_time_in_month')],
            [types.InlineKeyboardButton(text="Среднее время обработок (прошлый месяц)",
                                        callback_data='choice_worker_sort_' + 'sum_time_in_last_month')]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard


# -----Keyboards for users-----

class NoticeKeyboards:
    @staticmethod
    def url_on_message(chat_id,message_id,thread_id=None):
        url= tools.get_url_on_message_from_parametrs(chat_id, message_id, thread_id)
        buttons = [
            [types.InlineKeyboardButton(text="Обработать", url=url)],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

class LogKeyboards:
    @staticmethod
    def url_on_message(url):
        buttons = [
            [types.InlineKeyboardButton(text="Обработать", url=url)],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

def get_keyboard_cmd_start():
    kb = [
        [
            types.KeyboardButton(text="Написать обрашение📝"),
            types.KeyboardButton(text="Мои обращения📋")
        ],
        [ types.KeyboardButton(text="Часто задаваемые вопросы📚") ],

    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите..."
    )
    return keyboard
def get_keyboard_choice_type_message():
    kb = [
        [
            types.KeyboardButton(text="Жалоба"),
            types.KeyboardButton(text="Вопрос")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите..."
    )
    return keyboard
def get_keyboard_get_photo():
    kb = [
        [
            types.KeyboardButton(text="Без изображения🖼"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите..."
    )
    return keyboard
def get_keyboard_send_message_or_not():
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите..."
    )
    return keyboard

def get_keyboard_after_send_message():
    kb = [
        [
            types.KeyboardButton(text="В главное меню"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите..."
    )
    return keyboard

def get_keyboard_page_list_empty():
    buttons = [
        [types.InlineKeyboardButton(text="Создать обращение", callback_data='create_message')],
        [types.InlineKeyboardButton(text="В главное меню", callback_data='main_menu')],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def get_keyboard_page_list(page,max_page,list_id:list=[]):

    buttons = []
    if max_page==1 and len(list_id)==0:
        buttons.append([types.InlineKeyboardButton(text="Создать обращение", callback_data='create_message')])
    else:
        for i in range(0,len(list_id)//2*2,2):
            buttons.append([types.InlineKeyboardButton(text=f"( {list_id[i]} )", callback_data=f'message_id_{list_id[i]}'),
                            types.InlineKeyboardButton(text=f"( {list_id[i+1]} )", callback_data=f'message_id_{list_id[i+1]}')])
        if len(list_id)%2!=0:
            buttons.append([types.InlineKeyboardButton(text=f"( {list_id[-1]} )", callback_data=f'message_id_{list_id[-1]}')])

        if page==1:
            buttons.append([types.InlineKeyboardButton(text="> Следующая >", callback_data='page_next')])
        elif page==max_page:
            buttons.append([types.InlineKeyboardButton(text="< Предыдущая <", callback_data='page_last')])
        else:
            buttons.append([types.InlineKeyboardButton(text="< Предыдущая <", callback_data='page_last'),
                        types.InlineKeyboardButton(text="> Следующая >", callback_data='page_next')])
    buttons.append([types.InlineKeyboardButton(text="В главное меню", callback_data='main_menu')])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

