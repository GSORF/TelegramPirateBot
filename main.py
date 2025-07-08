import os
import logging
from telegram import Update, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
    CommandHandler,
    JobQueue,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# In-memory store of pending users: {(chat_id, user_id)}
pending_users = set()

async def greet_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Send a pirate-style greeting to each new member and schedule a check in 60 minutes.
    """
    chat_id = update.effective_chat.id
    for member in update.message.new_chat_members:
        user_id = member.id
        # Mark user as pending
        pending_users.add((chat_id, user_id))
        # Pirate greeting
        text = (
            f"🏴‍☠️ Ahoy, {member.full_name}! Willkommen an Bord! "
            "Innerhalb von 60 Minuten musst du ein persönliches Wort an die Crew richten, "
            "ansonsten wird dein Ticket gekielholt! ⚓️"
        )
        await context.bot.send_message(chat_id=chat_id, text=text)
        # Schedule a check in 60 minutes
        context.job_queue.run_once(
            callback=check_pending_user,
            when=60 * 60,
            chat_id=chat_id,
            data=user_id,
            name=f"check_{chat_id}_{user_id}"
        )

async def personal_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    When a pending user sends any text message (excluding commands), mark them as verified.
    """
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    key = (chat_id, user_id)
    if key in pending_users:
        pending_users.remove(key)
        logger.info(f"User {user_id} in chat {chat_id} has been verified.")

async def check_pending_user(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Kick users who are still pending after 60 minutes.
    """
    job = context.job
    chat_id = job.chat_id
    user_id = job.data
    key = (chat_id, user_id)
    if key in pending_users:
        try:
            await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
            logger.info(f"Kicked user {user_id} from chat {chat_id} due to inactivity.")
        except Exception as e:
            logger.error(f"Fehler beim Kicken von Nutzer {user_id}: {e}")
        pending_users.remove(key)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Basic /start command in private chat to test the bot.
    """
    await update.message.reply_text(
        "Pirate Spam Guard an Deck! Ich bewache deine Gruppe vor Bots!"
    )


def main() -> None:
    """
    Start the bot.
    """
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("Bitte setze die Umgebungsvariable TELEGRAM_BOT_TOKEN.")
        return

    # Build application
    app = ApplicationBuilder().token(token).build()

    # Handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_members))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, personal_message))

    # Run the bot
    logger.info("Starte Pirate Spam Guard Bot...")
    app.run_polling()


if __name__ == '__main__':
    main()
