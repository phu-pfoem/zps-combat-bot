from typing import Optional

from telegram import Update


def get_relevant_info(update: Update) -> Optional[tuple[int, int, str]]:
    try:
        message = update.message
        return update.message.chat.id, update.message.message_id, message.text.encode('utf-8').decode()
    except AttributeError:
        return None
