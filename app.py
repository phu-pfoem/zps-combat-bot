import re
from time import sleep

from flask import Flask, request
import telegram

import utils
from command import send_welcome_msg
from telebot.credentials import bot_token, bot_url

bot = telegram.Bot(token=bot_token)
app = Flask(__name__)
_command_map = {
    '/start': send_welcome_msg,
}


@app.route('/{}'.format(bot_token), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id, msg_id, text = utils.get_relevant_info(update)

    # the first time you chat with the bot AKA the welcoming message
    if text in _command_map:
        _command_map.get(text)(bot=bot, chat_id=chat_id, msg_id=msg_id)
    else:
        # noinspection PyBroadException
        try:
            # clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)
            # create the api link for the avatar based on http://avatars.adorable.io/
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
            # reply with a photo to the name the user sent,
            # note that you can send photos by url and telegram will fetch it for you
            bot.sendChatAction(chat_id=chat_id, action="upload_photo")
            sleep(2)
            bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
        except Exception:
            # if things went wrong
            bot.sendMessage(chat_id=chat_id,
                            text="There was a problem in the name you used, please enter different name",
                            reply_to_message_id=msg_id)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{url}{hook}'.format(url=bot_url, hook=bot_token))

    if s:
        return "ok" + '{url}{hook}'.format(url=bot_url, hook=bot_token)
    else:
        return "failed"


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hi, Mị là ZPS Combat Bốt, với sứ mệnh giúp mụi ngừ combat thật zui ó \U0001F449\U0001F448"


if __name__ == '__main__':
    app.run(threaded=True)
