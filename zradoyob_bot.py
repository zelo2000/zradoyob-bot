import logging

from telegram import ForceReply, Update, InputMediaPhoto, InputMediaAnimation
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("You can write /zrada @username to indicate zradoyob.\n You can write /help to get instructions how to use bot.\n You can use /start to ... because abrycos.")


async def zrada_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /zrada is issued."""
    if len(context.args) != 1:
        update.message.reply_text('Usage: /zrada @username')
        return

    username = context.args[0]

    if not username.startswith('@'):
        update.message.reply_text('Please mention a valid username with @')
        return

    chat_id = update.message.chat_id
    # Replace with your own URLs or paths to the GIF and image
    mp4_path = './files/gif.mp4'
    image_path = './files/image.jpg'

    with open(mp4_path, 'rb') as mp4_file:
        await context.bot.send_animation(chat_id=chat_id, animation=mp4_file, caption=f'{username}')

    with open(image_path, 'rb') as image_file:
        await context.bot.send_photo(chat_id=chat_id, photo=image_file)


# TODO: Add NLP model to process messages and say where is Zrada
# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Echo the user message."""
#     await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("TOKEN").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("zrada", zrada_command))

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
