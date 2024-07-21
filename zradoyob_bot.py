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
    await update.message.reply_text("You can write /zrada @username to indicate zradoyob.")


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
    gif_url = 'https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif'
    image_url = 'https://example.com/your-image.jpg'

    media = [
        InputMediaAnimation(
            media=gif_url, caption=f'{username}, here is your GIF!'),
        InputMediaPhoto(media=image_url,
                        caption=f'{username}, here is your image!')
    ]

    context.bot.send_media_group(chat_id=chat_id, media=media)


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
