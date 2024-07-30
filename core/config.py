import configparser  # импортируем библиотеку
from core.tools.Supdict import Sdict

CONFIG_DIR = "core/config.ini"


def is_number(string):
    try:
        float(string)
        return True
    except:
        return False


def Configurator():
    config_class = configparser.ConfigParser()  # создаём объекта парсера
    config_class.read(CONFIG_DIR)  # читаем конфиг

    defaults = config_class.defaults()
    if defaults != dict():
        config_dict = dict(defaults)
        for old_key, value in config_dict.items():
            new_key = old_key.upper()
            config_dict[new_key] = config_dict.pop(old_key)
            if is_number(config_dict[new_key]):
                config_dict[new_key] = int(config_dict[new_key])
    else:
        config_dict = dict()
        sections = config_class.sections()
        for section in sections:
            items = config_class.items(section)
            d=dict()
            for old_key, value in items:
                new_key = old_key.upper()
                d[new_key] = value
                if is_number(d[new_key]):
                    d[new_key] = int(d[new_key])
            config_dict[section] = d

    print(config_dict)

    return Sdict(config_dict)

config = Configurator()
