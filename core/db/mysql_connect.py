from mysql.connector import connect
from mysql.connector import Error as ConnectorError
import datetime
import hashlib
import logging

DATABASE_NAME = 'project_4'#'notice_bot'
DATABASE_USER_NAME = 'admin'#'app'
DATABASE_USER_PASS = 'admin'#'%M8PB}n3'

class MySqlDatabase:
    def __init__(self,link,database):
        self.link_database=link
        self.user=DATABASE_USER_NAME
        self.password=DATABASE_USER_PASS
        self.database=database
        self.port = 3306


    def __connect(self):
        return connect(
                    host=self.link_database,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
            )
    def __get_processed_value_with_operator(self,value):
        if value is None or value=='NULL':
            return 'IS NULL'
        elif value=='NOT NULL':
            return ' IS NOT NULL'
        elif isinstance(value,int):
            return f"= {value}"
        elif isinstance(value,str):
            return f"= \"{value}\""
        elif isinstance(value,datetime.datetime):
            return f"= \"{value.strftime('%Y-%m-%d %H:%M:%S')}\""
        else:
            return '=NULL'
    def __get_processed_value(self,value):
        if value is None or value=='NULL':
            return 'NULL'
        elif value=='NOT NULL':
            return 'IS NOT NULL'
        elif isinstance(value,int):
            return f"{value}"
        elif isinstance(value,str):
            return f"\"{value}\""
        elif isinstance(value,datetime.datetime):
            return f"\"{value.strftime('%Y-%m-%d %H:%M:%S')}\""
        else:
            return value
    def request(self,text_request:str,isSave=False):
        try:
            with self.__connect() as conn:
                logging.debug(f"MYSQL QUERY: {text_request}")
                cursor_database = conn.cursor()
                cursor_database.execute(text_request)
                if isSave:
                    conn.commit()
                data = cursor_database.fetchall()
                logging.debug(f"MYSQL Result: {data}")
            return data
        except ConnectorError as e:
            logging.error("MySql Error 500"+' : '+str(e))
            return []

    def add(self,table: str,**kwargs: dict):
        if not (kwargs.get('__arg') is None):
            kwargs=kwargs.get('__arg')
        if self.check(table,__arg=kwargs):
            status=False
        else:
            request = f'''INSERT INTO {table} ({','.join(kwargs.keys())}) 
    VALUES ({','.join(map(lambda x: self.__get_processed_value(x),kwargs.values()))});'''
            result = self.request(request,isSave=True)
            status = True
        return status
    def multi_add(self,table: str,**kwargs: dict):
        if not (kwargs.get('__arg') is None):
            kwargs = kwargs.get('__arg')
        status = False
        try:
            data = list(zip(*kwargs.values()))
            col_names = list(kwargs.keys())
            for values in data:
                d = dict()
                for i in range(len(col_names)):
                    d[col_names[i]]=values[i]
                f = self.add(table,__arg=d)
                if f:
                    status=True
        except Exception as e:
            logging.error("Ошибка 500"+' : '+str(e))
            status = False
        finally:
            return status
    def edit(self,table: str,where: dict,**kwargs):
        if not (kwargs.get('__arg') is None):
            kwargs = kwargs.get('__arg')
        if not self.check(table, __arg=where):
            status = False
        else:
            request = f"UPDATE {table}\n"
            request += "SET "
            max_i = len(kwargs.keys())
            i = 0
            for key, value in kwargs.items():
                if i == max_i - 1:
                    request += f'{key}="{value}"\n'
                else:
                    request += f'{key}="{value}", '
                i += 1
            max_i = len(where)
            i = 0
            for key, value in where.items():
                if i == 0:
                    request += f"WHERE {key} {self.__get_processed_value_with_operator(value)} "
                elif i == max_i - 1:
                    request += f'AND {key} {self.__get_processed_value_with_operator(value)}\n'
                else:
                    request += f'AND {key} {self.__get_processed_value_with_operator(value)} '
                i += 1
            request += ';'
            result = self.request(request,isSave=True)
            status = True
        return status




    def search_n(self, table: str,step=1,count=1,sort_name=None, **kwargs):
        if not (kwargs.get('__arg') is None):
            kwargs = kwargs.get('__arg')
        request = f"""SELECT * FROM {table}\n"""
        if kwargs != dict():
            max_i = len(kwargs.keys())
            i = 0
            for key, value in kwargs.items():
                if i == 0:
                    request += f"WHERE {key} {self.__get_processed_value_with_operator(value)} "
                elif i == max_i - 1:
                    request += f'AND {key} {self.__get_processed_value_with_operator(value)}\n'
                else:
                    request += f'AND {key} {self.__get_processed_value_with_operator(value)} '
                i += 1
        if not (sort_name is None):
            request += f"""ORDER BY {sort_name} ASC \n"""
        if not (count is None):
            request += f"LIMIT {(step - 1) * count}, {count}"

        if request.endswith('\n'):
            request=request[:-1]
        request += ';'
        result =self.request(request)
        return result

    def count(self, table: str, **kwargs):
        if not (kwargs.get('__arg') is None):
            kwargs=kwargs.get('__arg')
        text = list(kwargs.values())[0]
        request = f"""SELECT count(*) FROM {table}\n"""
        max_i = len(kwargs.keys())
        i = 0
        for key, value in kwargs.items():
            if i == 0:
                request += f"WHERE {key} {self.__get_processed_value_with_operator(value)} "
            elif i == max_i - 1:
                request += f'AND {key} {self.__get_processed_value_with_operator(value)}\n'
            else:
                request += f'AND {key} {self.__get_processed_value_with_operator(value)} '
            i += 1
        result = self.request(request)
        if result==[]:
            return 0
        count=result[0][0]
        return count


    def delete(self, table: str, **kwargs):
        if not (kwargs.get('__arg') is None):
            kwargs=kwargs.get('__arg')
        if not self.check(table, __arg=kwargs):
            status = False
        else:
            text = list(kwargs.values())[0]
            request = f"DELETE FROM {table}\n"+f"WHERE {str(list(kwargs.keys())[0])} {self.__get_processed_value_with_operator(text)};"
            result = self.request(request,isSave=True)
            status = False if result is None else True
        return status
    def multi_delete(self,table: str,**kwargs):
        if not (kwargs.get('__arg') is None):
            kwargs = kwargs.get('__arg')
        status = False
        try:
            data = list(zip(*kwargs.values()))
            col_names = list(kwargs.keys())
            for values in data:
                d = dict()
                for i in range(len(col_names)):
                    d[col_names[i]]=values[i]
                f= self.delete(table,__arg=d)
                if f:
                    status=True
        except Exception as e:
            logging.error("Ошибка 500"+' : '+str(e))
            status = False
        finally:
            return status
    def count_all(self, table: str):

        request = f"""SELECT count(*) FROM {table};"""
        result = self.request(request)
        if result==[]:
            return 0
        count = result[0][0]
        return count
    def check(self,table: str,**kwargs) :
        if not (kwargs.get('__arg') is None):
            kwargs = kwargs.get('__arg')
        request = f"SELECT * FROM {table}\n"
        max_i = len(kwargs)
        i = 0
        for key, value in kwargs.items():
            if i == 0:
                request += f"WHERE {key} {self.__get_processed_value_with_operator(value)} "
            elif i == max_i - 1:
                request += f"AND {key} {self.__get_processed_value_with_operator(value)}"
                break
            else:
                request += f"AND {key} {self.__get_processed_value_with_operator(value)} "
            i += 1
        request+=';'
        result = self.request(request)
        status = False if len(result)==0 else True
        return status

mysql=MySqlDatabase('localhost',DATABASE_NAME)
