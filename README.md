# Telegram bot template

[RU](RU_README.md)

**!!! Attention: at the moment, the template does not run out of the box, work is underway on this**

A template with a volumetric structure and a stack of technologies for developing a Telegram bot using the Aiogram library

## Installation

1. Installing and deploying the code
```bash
git clone https://github.com/TimurRoss/aiogram-bot-example.git # Cloning the repository

python -m venv venv # Creating a virtual environment

# For Linux
source venv/bin/activate
# For Windows cmd
venv\Scripts\activate.bat

pip install -r requirements.txt # Installing all the necessary libraries
```

2. Entering confidential data

In the `core/config.ini` file, the following parameters must be filled in:
* ADMIN_IDS - admin id numbers (for access to the admin panel), separated by commas
* BOT_TOKEN - bot token that can be obtained from BotFather(see [here](https://core.telegram.org/bots/features#botfather ))
* NOTICE_CHANNEL - channel id for interactions

3. Running the script
``` bash
python main.py # Bot Launches
```


## Bot structure

``` graph
- main.py - the main executable file
- requirements.txt - a file with a list of required libraries
- /core - the folder where the main code of the bot
is located - bot.py - a bot class is being created in it
- config.py - pulls up the parameters from the `config.ini` file
    - keyboards.py - it contains all inline and regular buttons
    - logger_setup.py - setting up log
processing - states.py - lists of states for finite state machines
- /db - folder with functions for working with different databases
- /filters - folder with its own filters 
    - /middleware - folder with your middleware
    - /scheduler - folder with handlers for "timer actions"
- /texts - folder with texts for messages
- /tools - folder with additional tools
```

That's all for now)