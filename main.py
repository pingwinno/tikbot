import logging
import os
import re

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, filters, MessageHandler

import tt_downloader

bot_token = os.environ['APIKEY']

application = ApplicationBuilder().token(bot_token).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tt_url = update.message.text
    print(tt_url)
    chat_id = update.message.chat_id
    out_message = await context.bot.send_message(chat_id=chat_id, text="Processing...")
    try:
        video_name = tt_downloader.get_video(tt_url)

        await context.bot.send_video(chat_id, f'./{video_name}',
                                     reply_to_message_id=update.message.message_id)
        await out_message.delete()
        print(video_name)
        tt_downloader.remove_video(video_name)
    except Exception as err:
        await context.bot.send_message(chat_id=chat_id, text=f"Error: {err}",
                                       reply_to_message_id=update.message.message_id)


if __name__ == '__main__':
    incorrect_import_handler = MessageHandler(filters.Regex(re.compile(r'https://vm\.tiktok\.com/.*')), start)
    application.add_handler(incorrect_import_handler)
    application.run_polling()
