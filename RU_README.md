# Шаблон для телеграм бота 

**!!! Внимание: на данный момент шаблон не запускается из коробки, ведется работа над этим**

Шаблон с объемной структурой и стеком технологий для разработки Telegram бота, с помощью библиотеки Aiogram

## Установка

1. Установка и развертываание кода
```bash
git clone https://github.com/TimurRoss/aiogram-bot-example.git # Клонируем репозиторий

python -m venv venv # Создаем виртуальное окружение

# Для Linux
source venv/bin/activate
# Для Windows cmd
venv\Scripts\activate.bat

pip install -r requirements.txt # Устанавливаем все необходимые библиотеки
```

2. Ввод конфиденциальных данных

В файле `core/config.ini`, необходимо заполнить следующие параметры:
* ADMIN_IDS - номера id админов(для доступа к админ панели), перечисляемые через запятую
* BOT_TOKEN - токен бота, который можно получить у BotFather(см. [сюда](https://core.telegram.org/bots/features#botfather))
* NOTICE_CHANNEL - id канала для взаимодействий

3. Запуск скрипта
``` bash
python main.py # Запускам бота
```


## Структура бота

``` graph
- main.py - главный исполняемый файл
- requirements.txt - файл со списком необходимых библиотек
- /core - папка, в которой лежит основной код бота
    - bot.py - в нем создается класс бота
    - config.py - подтягивает параметры из файла `config.ini`
    - keyboards.py - в нём расположены все inline и обычные кнопки
    - logger_setup.py - настройка обработика логов
    - states.py - списки состояний для конечных автоматов
    - /db - папка с функциями для работами с разными базами данных
    - /filters - папка со своими фильтрами 
    - /middleware - папка со своими мидльварями
    - /scheduler - папка с обработчиками "действий по таймеру"
    - /texts - папка с текстами для сообщений
    - /tools - папка с доп. инструментами
```

Пока на этом всё)