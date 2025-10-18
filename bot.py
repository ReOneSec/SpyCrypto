import re
import os
import logging
from dotenv import load_dotenv  # To load .env file
from telegram import Update, ChatMemberStatus
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from telegram.error import Forbidden, BadRequest

# --- Load Environment Variables ---
# This line loads the .env file into the environment
load_dotenv()

# --- Setup Logging ---
# Configures logging to provide timestamped, leveled messages.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# Get a logger instance for this module
logger = logging.getLogger(__name__)

# --- BOT TOKEN (Loaded from environment) ---
# Load the token from an environment variable for security.
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    logger.critical("CRITICAL: No TELEGRAM_TOKEN environment variable set! Exiting.")
    exit(1) # Exit if no token is found

# --- REGEX PATTERNS ---
# Define patterns for common crypto addresses.
ETH_PATTERN = r"0x[a-fA-F0-9]{40}"
BTC_LEGACY_PATTERN = r"[13][a-km-zA-HJ-NP-Z1-9]{25,34}" # Legacy P2PKH/P2SH
BTC_BECH32_PATTERN = r"bc1[a-zA-HJ-NP-Z0-9]{38,58}" # Modern Bech32/Bech32m
SOL_PATTERN = r"[1-9A-HJ-NP-Za-km-z]{32,44}"

# Combine all patterns into one, separated by | (which means "OR")
# We use re.IGNORECASE to make it case-insensitive
# We use \b (word boundary) to ensure we're matching whole addresses
ADDRESS_REGEX = re.compile(
    rf"\b({ETH_PATTERN}|{BTC_LEGACY_PATTERN}|{BTC_BECH32_PATTERN}|{SOL_PATTERN})\b", 
    re.IGNORECASE
)

# --- THE MESSAGE HANDLER ---
async def check_for_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Checks incoming text messages for crypto addresses and deletes them
    if the user is not an admin.
    """
    message = update.message
    
    # 1. Ignore non-text messages or messages without a user (e.g., channel posts)
    if not message or not message.text or not message.from_user:
        return 

    chat_id = message.chat_id
    user = message.from_user
    user_id = user.id

    # 2. Check if the message is from an admin. If so, ignore it.
    try:
        chat_member = await context.bot.get_chat_member(chat_id, user_id)
        
        # Use the ChatMemberStatus enum for robust checking
        if chat_member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
            logger.info(f"Ignoring admin message from {user.username or user.id} in chat {chat_id}")
            return
            
    except Exception as e:
        logger.error(f"Error checking admin status for {user_id} in {chat_id}: {e}", exc_info=True)
        # --- SAFER FAILSAFE ---
        # If we can't check status (e.g., API error), DO NOT delete the message.
        # It's better to let a potential spam message pass than to delete an admin's post.
        logger.warning(f"Could not verify admin status for {user_id}. Ignoring message as a precaution.")
        return

    # 3. Search for any of our address patterns in the message text
    if ADDRESS_REGEX.search(message.text):
        logger.info(f"Found address in message from {user.username or user.id}. Deleting...")
        
        try:
            # --- Action 1: DELETE the message ---
            await context.bot.delete_message(
                chat_id=message.chat_id,
                message_id=message.message_id
            )

            # --- Action 2: Notify the user ---
            # Create a "mention" for the user that works even if they have no username.
            user_mention = user.mention_markdown_v2(user.full_name)
            
            # Send a polite notification to the chat.
            await context.bot.send_message(
                chat_id=message.chat_id,
                text=f"{user_mention}, your message was automatically removed because it appears to contain a cryptocurrency address\. Posting addresses is not allowed here\.",
                parse_mode=ParseMode.MARKDOWN_V2
            )

            # --- Optional Action 3: Ban the user ---
            # Uncomment the following lines to ban the user instead of just warning them.
            # await context.bot.ban_chat_member(
            #     chat_id=message.chat_id,
            #     user_id=message.from_user.id
            # )
            # logger.info(f"Banned user {user.username or user.id} for posting address.")

        except Forbidden:
            logger.warning(f"Failed to delete message: Bot does not have 'delete' permissions in chat {chat_id}.")
        except BadRequest as e:
            if "message to delete not found" in str(e):
                logger.warning(f"Message {message.message_id} was already deleted.")
            else:
                logger.error(f"Failed to delete/notify: {e}", exc_info=True)
        except Exception as e:
            # Catch other potential errors (e.g., user blocked bot, can't send notify)
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)

# --- MAIN FUNCTION TO RUN THE BOT ---
def main():
    """
    Starts the bot, adds the message handler, and begins polling.
    """
    logger.info("Bot starting...")
    
    # Build the application using the token
    application = Application.builder().token(TOKEN).build()

    # Create a handler that listens to *all* text messages
    # filters.TEXT & (~filters.COMMAND) means "any text that is NOT a command"
    address_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), check_for_address)
    
    # Add the handler to the application
    application.add_handler(address_handler)

    # Start polling for new messages
    logger.info("Bot polling started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
              
