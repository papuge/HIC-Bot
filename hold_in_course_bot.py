import logging
import os
import sys
import config

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")


if mode == "dev":
    def run(updater):
        updater.start_polling()
# elif mode == "prod":
#     def run(updater):
#         PORT = int(os.environ.get("PORT", "8443"))
#         HOLD_IN_COURSE_BOT = os.environ.get("HOLD_IN_COURSE_BOT")
#         updater.start_webhook(listen="0.0.0.0",
#                               port=PORT,
#                               url_path=TOKEN)
#         updater.bot.set_webhook(f"https://{HOLD_IN_COURSE_BOT}."
#                                 f"herokuapp.com/{TOKEN}")
else:
    sys.exit(1)


def start_handler(bot, update):
    logger.info(f"User {update.effective_user['id']} started bot")

    if update.message.chat.id in config.zai:
        update.message.reply_text("Стэй виз ми, мя зя " + config.orange_heart)
    else:
        update.message.reply_text(f"Приветики, "
                                  f"{update.effective_user['username']}!")


def sss_handler(bot, update):
    if update.message.chat.id in config.zai:
        keyboard = [[
            InlineKeyboardButton(config.doughnut_unicode, callback_data='d'),
            InlineKeyboardButton(config.fountain_unicode, callback_data='p'),
            InlineKeyboardButton(config.shower_unicode, callback_data='18')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("уляля :з", reply_markup=reply_markup)


def sss_callback(bot, update):
    query = update.callback_query
    logger.info(f"User {query.message.chat.id} send message")
    receiver = (config.zai[1] if query.message.chat.id == config.zai[0]
                else config.zai[0])

    if query.data == "d":
        emoji = config.doughnut_unicode
    elif query.data == "p":
        emoji = config.fountain_unicode
    else:
        emoji = config.shower_unicode

    bot.send_message(chat_id=receiver, text="Зая только что " + emoji)
    query.answer(text='ыыыыы')
    logger.info(f"User {receiver} received message")


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("sss", sss_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(sss_callback))

    run(updater)
