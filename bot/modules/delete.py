import threading

from telegram.ext import CommandHandler

from bot import dispatcher, LOGGER
from bot.helper.mirror_utils.upload_utils import gdriveTools
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import auto_delete_message, sendMessage


def deletefile(update, context):
    msg_args = update.message.text.split(None, 1)
    msg = ''
    try:
        link = msg_args[1]
        LOGGER.info(msg_args[1])
    except IndexError:
        msg = '𝐒𝐞𝐧𝐝 𝐚 𝐥𝐢𝐧𝐤 𝐚𝐥𝐨𝐧𝐠 𝐰𝐢𝐭𝐡 𝐜𝐨𝐦𝐦𝐚𝐧𝐝'

    if msg == '':
        drive = gdriveTools.GoogleDriveHelper()
        msg = drive.deletefile(link)
    LOGGER.info(f"DeleteFileCmd : {msg}")
    reply_message = sendMessage(msg, context.bot, update)

    threading.Thread(target=auto_delete_message, args=(context.bot, update.message, reply_message)).start()


delete_handler = CommandHandler(command=BotCommands.DeleteCommand, callback=deletefile,
                                filters=CustomFilters.owner_filter | CustomFilters.sudo_user
                                and CustomFilters.login_user, run_async=True)

dispatcher.add_handler(delete_handler)
