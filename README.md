# Telegram Bot (Memes generator)

___Info___

This bot takes photo from telegram user and add random funny phrase on this image (pool of phrase is customizable).
You can add this bot to group and when bot complete to draw on picture - you can send new picture to other group (customizable).

___Registration of new bot___
1. You should to write @botfather in telegram and register new bot.
2. Choose name, adress of your bot and write your API TOKEN.
3. Be sure that your bot is available for group. Write to @botfather
	* /mybots -> bot_name -> bot settings -> allow groups -> enable mode
	* /mybots -> bot_name -> bot settings -> group privacy -> disable mode

___Settings___

All settings could be edit in .env file in base folder.

TELEGRAM_TOKEN - your telegram token getting from @botfather.

IMG_FOLDER - folder where bot will be save users images.

PHRASE_FILE_DIR - way to 'phrase_list.txt' file with pool of available phrases. You could also edit this file.

FONT_DIR - way to font file.

MAX_WIDTH_OF_TEXT - max width of text block on image in percent (%) from original image width (recomended 80%)

MAX_HEIGHT_OF_TEXT - max height of text block on image in percent (%) from original image height (recomended 25%)

CHAT_FOR_RESEND - chat_id in which bot will be resend pictures if user will choose this

___Development__
Docker, Docker-compose should be install on your host

a) To start bot on your host just run:
`make start`
It will build image and create docker container.

b) To stop container with bot just run:
`make stop`

b) To prepare unit tests:
`make inst-pytest` 
This command will instal pytest library in your docker container. Be sure that your container is active.

c) To run uint test:
'make test'
It will collect testfiles and run them as though it was started from base project directory.
