import random
from time import sleep

from telegram import Bot


def send_welcome_msg(bot: Bot, chat_id: int, msg_id: int):
    # the welcoming message
    bot_welcome = "Hi, Mị là ZPS Combat Bốt, với sứ mệnh giúp mụi ngừ combat thật zui ó \U0001F449\U0001F448"

    # send the welcoming message
    bot.sendChatAction(action="typing", chat_id=chat_id)  # Hesitant feelings
    sleep(random.random() * 1.0 + 0.5)
    bot.sendMessage(text=bot_welcome, chat_id=chat_id, reply_to_message_id=msg_id)
