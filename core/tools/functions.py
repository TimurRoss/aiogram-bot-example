import datetime
import logging
from aiogram import types, Bot, md
from core import config
from core.db.mysql_connect import mysql
from core.bot import bot


# ------MYSQL Functions-------

def worker_list_parametrs_to_dict(worker_list_parametrs):
    d = dict()
    d['id'] = worker_list_parametrs[0]
    d['login'] = worker_list_parametrs[0]


def update_statistics():
    logging.info('UPDATE STATISTICS STARTED')
    time_start_update_start = datetime.datetime.now()
    list_workers = mysql.search_n('workers', count=None)
    for worker in list_workers:
        worker_login = get_worker_login((worker,))
        data = {'day':
                    {"text_mysql1": '1 DAY',
                     "text_mysql2": 'NOW()',
                     'sum_time_processing': 0,
                     'count_processed_message': 0},
                'week':
                    {"text_mysql1": '1 WEEK',
                     "text_mysql2": 'NOW()',
                     'sum_time_processing': 0,
                     'count_processed_message': 0},
                'month':
                    {"text_mysql1": '1 MONTH',
                     "text_mysql2": 'NOW()',
                     'sum_time_processing': 0,
                     'count_processed_message': 0},
                'last_month':
                    {"text_mysql1": '2 MONTH',
                     "text_mysql2": 'DATE_SUB(NOW(),INTERVAL 1 MONTH)',
                     'sum_time_processing': 0,
                     'count_processed_message': 0},
                }
        for name_period, period_data in data.items():
            result = mysql.request('SELECT * FROM messages\n'
                                   f'WHERE worker_login = "{worker_login}"\n'
                                   f'AND time_send >= DATE_SUB(NOW(),INTERVAL {period_data["text_mysql1"]})\n'
                                   f'AND time_send < {period_data["text_mysql2"]};')
            data[name_period]['count_processed_message'] = len(result)
            for i in result:
                if i[4] == None:
                    continue
                data[name_period]['sum_time_processing'] += int((i[4] - i[3]).total_seconds())
        if not mysql.check('statistics', login=worker_login):
            mysql.add('statistics',
                      login=worker_login,
                      count_in_day=data['day']['count_processed_message'],
                      count_in_week=data['week']['count_processed_message'],
                      count_in_month=data['month']['count_processed_message'],
                      count_in_last_month=data['last_month']['count_processed_message'],
                      sum_time_in_day=data['day']['sum_time_processing'],
                      sum_time_in_week=data['week']['sum_time_processing'],
                      sum_time_in_month=data['month']['sum_time_processing'],
                      sum_time_in_last_month=data['last_month']['sum_time_processing'])
        else:
            mysql.edit('statistics',
                       where={'login': worker_login},
                       count_in_day=data['day']['count_processed_message'],
                       count_in_week=data['week']['count_processed_message'],
                       count_in_month=data['month']['count_processed_message'],
                       count_in_last_month=data['last_month']['count_processed_message'],
                       sum_time_in_day=data['day']['sum_time_processing'],
                       sum_time_in_week=data['week']['sum_time_processing'],
                       sum_time_in_month=data['month']['sum_time_processing'],
                       sum_time_in_last_month=data['last_month']['sum_time_processing'])
    mysql.request('DELETE FROM messages\n'
                  f'WHERE time_send < DATE_SUB(NOW(),INTERVAL 2 MONTH);')
    logging.info(f'UPDATE STATISTICS FINISHED (TIME: {datetime.datetime.now() - time_start_update_start})')


# ------Personal Functions-------

def state_data_is_empty(user_data):
    return True if user_data == dict() else False


def create_start_state_data():
    return {'page_list_workers': 1,
            'page_list_providers': 1,
            'sort_workers': 'count_in_day'}


def get_small_text(text: str, n=10):
    small_text = text if len(text) < n else text[:n]
    small_text = small_text.replace('\n', '').replace('\t', '')
    return small_text


def constrain(x, min_, max_):
    if x < min_:
        return min_
    elif x > max_:
        return max_
    else:
        return x


def get_string_list_message_workers(list_message):
    string = ''
    for i in list_message:
        text = i[0]
        string += f'\* {md.quote(text)}\n\n'
    string = string[:-1]
    return string


def get_from_message_list_workers(message: str):
    l = message.split(',')
    for i in range(len(l)):
        l[i] = l[i].strip()
        if not l[i].startswith('@'):
            l[i] = '@' + l[i]
    return l


def get_string_list_message_providers(list_message):
    string = ''
    for i in list_message:
        id = i[0]
        id_providers = i[1]
        add_id_providers = i[2]
        if add_id_providers is None:
            string += f'"{id}"\n{id_providers}\n\n'
        else:
            string += f'"{id}"\n{id_providers} ({add_id_providers})\n\n'
    string = string[:-1]
    return string


def get_from_message_list_providers(message: str):
    l = message.split(',')
    l2 = ['NULL' for i in range(len(l))]
    for i in range(len(l)):
        if '(' in l[i]:
            k = l[i].split('(')
            k[1] = k[1].replace(')', '')
            k[0] = k[0].strip()
            k[1] = k[1].strip()
            l[i] = k[0]
            l2[i] = k[1]
        else:
            l[i] = l[i].strip()
    return l, l2


def get_from_message_list_providers_to_delete(message: str):
    l = message.split(',')
    for i in range(len(l)):
        l[i] = l[i].strip()
    return l


def is_message_processed(request: list) -> bool:
    if request == [] or request == [tuple()]:
        return True
    if request[0][5] == None:
        return False
    else:
        return True


def get_count_add_messages_on_notice(request):
    return request[0][7]


def get_time_send(request):
    return request[0][3]


def get_notice_id(request):
    return request[0][6]


def get_chat_id(request):
    return request[0][2]


def get_message_id(request):
    return request[0][1]


def get_worker_login(request):
    return request[0][1]


def get_url_on_message_from_parametrs(chat_id, message_id, thread_id=None):
    if str(chat_id).startswith('-100'):
        chat_id = str(chat_id).replace('-100', '')
    url = ''
    if thread_id is None:
        url = f"https://t.me/c/{chat_id}/{message_id}"
    else:
        url = f"https://t.me/c/{chat_id}/{message_id}?thread={thread_id}"
    return url


async def delete_keyboard_for_time(notice_id: int, count_add_messages: int):
    request = mysql.search_n('messages', notice_id=notice_id)
    if count_add_messages == get_count_add_messages_on_notice(request):
        await bot.edit_message_reply_markup(chat_id=int(config.NOTICE_CHANNEL),
                                            message_id=notice_id,
                                            reply_markup=None)


async def delete_message_for_time(notice_id: int):
    try:
        await bot.delete_message(chat_id=int(config.NOTICE_CHANNEL),
                                 message_id=notice_id)
    except:
        logging.warn(f'Сообщение с id = {notice_id} не может быть удалено')


async def send_log_message(chat_name: str, url_keyboard: types.InlineKeyboardMarkup, login: str,
                           datetime_send: datetime.datetime, count_add_messages: int, time_send):
    await bot.send_message(chat_id=int(config.LOG_CHANNEL),
                           text=f'+{count_add_messages} 📩 от поставщика "{md.quote(chat_name)}"\n\n✅ Просмотрено:\n{md.quote(login)}, {md.quote(datetime_send.strftime("%d.%m.%Y, %H:%M:%S"))}\nВремя обработки: {round((datetime.datetime.now() - time_send).total_seconds())} сек.',
                           reply_markup=url_keyboard)
