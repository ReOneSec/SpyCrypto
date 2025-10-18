import re
import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo import MongoClient

from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from telegram.constants import ParseMode, ChatMemberStatus
from telegram.error import Forbidden, BadRequest

# --- Load Environment & Basic Setup ---
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_LOG_CHANNEL = os.getenv("ADMIN_LOG_CHANNEL")

if not TOKEN or not MONGO_URI:
    logger.critical("CRITICAL: TOKEN and MONGO_URI must be set in .env! Exiting.")
    exit(1)

# --- Database Manager Class ---
class DatabaseManager:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.spyCryptoBot
        self.strikes = self.db.strikes
        self.actions = self.db.actions
        logger.info("MongoDB connection established.")

    def get_user_strikes(self, chat_id, user_id):
        user_doc = self.strikes.find_one({"chat_id": chat_id, "user_id": user_id})
        return user_doc['strike_count'] if user_doc else 0

    def increment_user_strikes(self, chat_id, user_id, username):
        self.strikes.update_one(
            {"chat_id": chat_id, "user_id": user_id},
            {"$inc": {"strike_count": 1}, "$set": {"username": username}},
            upsert=True
        )
        return self.get_user_strikes(chat_id, user_id)

    def log_action(self, chat_id, user_id, action, reason):
        self.actions.insert_one({
            "timestamp": datetime.now(),
            "chat_id": chat_id,
            "user_id": user_id,
            "action": action,
            "reason": reason
        })
        
    def get_stats(self, chat_id):
        seven_days_ago = datetime.now() - timedelta(days=7)
        query = {"chat_id": chat_id, "timestamp": {"gte": seven_days_ago}}
        
        deleted_count = self.actions.count_documents({**query, "action": "deleted"})
        muted_count = self.actions.count_documents({**query, "action": "muted"})
        banned_count = self.actions.count_documents({**query, "action": "banned"})
        
        return deleted_count, muted_count, banned_count

# --- Regex & Bot Data ---
# Dictionary keys are now user-friendly for generating the info message
PATTERNS = {
    "Ethereum (EVM chains)": r"0x[a-fA-F0-9]{40}",
    "Bitcoin (BTC)": r"[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-HJ-NP-Z0-9]{38,58}",
    "Litecoin (LTC)": r"[LM][a-km-zA-HJ-NP-Z1-9]{26,33}|ltc1[a-zA-HJ-NP-Z0-9]{39,59}",
    "Dogecoin (DOGE)": r"D[a-km-zA-HJ-NP-Z1-9]{33}",
    "Bitcoin Cash (BCH)": r"(bitcoincash:)?q[a-z0-9]{41}",
    "Dash (DASH)": r"X[1-9A-HJ-NP-Za-km-z]{33}",
    "Zcash (ZEC)": r"t1[a-km-zA-HJ-NP-Z1-9]{33}|z[a-km-zA-HJ-NP-Z1-9]{93}",
    "Solana (SOL)": r"[1-9A-HJ-NP-Za-km-z]{32,44}",
    "TRON (TRX)": r"T[a-zA-HJ-NP-Z1-9]{33}",
    "Polkadot (DOT)": r"1[a-zA-HJ-NP-Z1-9]{46,47}",
    "Ripple (XRP)": r"r[a-km-zA-HJ-NP-Z1-9]{25,34}",
    "Cardano (ADA)": r"addr1[a-z0-9]{98}|[DE][1-9A-HJ-NP-Za-km-z]{32,103}",
    "Monero (XMR)": r"4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}",
    "BNB Beacon Chain": r"bnb1[a-z0-9]{38}",
    "Avalanche (AVAX X-Chain)": r"X-[a-km-zA-HJ-NP-Z1-9]{44}",
    "Cosmos (ATOM)": r"cosmos1[a-z0-9]{38}",
    "Tezos (XTZ)": r"tz[1-3][a-km-zA-HJ-NP-Z1-9]{33}",
    "NEAR Protocol": r"[a-z0-9\._-]{2,64}\.near",
    "Stellar (XLM)": r"G[A-Z0-9]{55}",
    "Algorand (ALGO)": r"[A-Z2-7]{58}",
    "The Open Network (TON)": r"(?:-1|0):[a-fA-F0-9]{64}|[UEk][a-zA-Z0-9\-_]{47}"
}
ADDRESS_REGEX = re.compile(rf"\b({'|'.join(PATTERNS.values())})\b", re.IGNORECASE)

# --- Create the info message dynamically from the PATTERNS dictionary ---
CHAIN_LIST_TEXT = "\n".join([f"• {name}" for name in sorted(PATTERNS.keys())])
SUPPORTED_CHAINS_MESSAGE = (
    f"🛡️ *SpyCrypto Moderation Bot*\n\n"
    f"I keep this group clean by automatically detecting and removing spam\. "
    f"I scan new messages, edited messages, and links for unauthorized content\.\n\n"
    f"*I can detect addresses from hundreds of blockchains, including:*\n"
    f"{CHAIN_LIST_TEXT}"
)

db = DatabaseManager(MONGO_URI)

# --- Helper Functions ---
async def log_to_admin_channel(context: ContextTypes.DEFAULT_TYPE, message: str):
    if ADMIN_LOG_CHANNEL:
        try:
            await context.bot.send_message(chat_id=ADMIN_LOG_CHANNEL, text=message, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            logger.error(f"Failed to log to admin channel {ADMIN_LOG_CHANNEL}: {e}")

def get_user_mention(user):
    return user.mention_markdown_v2(user.full_name)
    
# --- Core Logic: Punishment System ---
async def process_spam(update: Update, context: ContextTypes.DEFAULT_TYPE, reason: str):
    """The main function to handle detected spam, apply strikes, and take action."""
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    
    try:
        await message.delete()
    except (BadRequest, Forbidden):
        logger.warning(f"Could not delete message {message.message_id} in chat {chat.id}. It may have been already deleted or I lack permissions.")
        return

    new_strike_count = db.increment_user_strikes(chat.id, user.id, user.username or "N/A")
    user_mention = get_user_mention(user)
    action_taken = "deleted"
    
    if new_strike_count == 1:
        warning_text = f"{user_mention}, posting unauthorized content is not allowed\. This is your first warning\."
        await context.bot.send_message(chat.id, warning_text, parse_mode=ParseMode.MARKDOWN_V2)
        action_taken = "warned"
    elif new_strike_count == 2:
        mute_duration = timedelta(days=1)
        try:
            await context.bot.restrict_chat_member(
                chat_id=chat.id, user_id=user.id,
                permissions={'can_send_messages': False},
                until_date=datetime.now() + mute_duration
            )
            mute_text = f"{user_mention}, you have received a second strike and are now muted for 24 hours\."
            await context.bot.send_message(chat.id, mute_text, parse_mode=ParseMode.MARKDOWN_V2)
            action_taken = "muted"
        except (Forbidden, BadRequest):
            logger.warning(f"No permission to mute users in chat {chat.id}")
    else:
        try:
            await context.bot.ban_chat_member(chat_id=chat.id, user_id=user.id)
            ban_text = f"{user_mention} has been banned after receiving three strikes\."
            await context.bot.send_message(chat.id, ban_text, parse_mode=ParseMode.MARKDOWN_V2)
            action_taken = "banned"
        except (Forbidden, BadRequest):
            logger.warning(f"No permission to ban users in chat {chat.id}")
            
    db.log_action(chat.id, user.id, action_taken, reason)
    log_message = (
        f"✅ *Action Taken in {chat.title}*\n\n"
        f"👤 *User:* {user_mention} `({user.id})`\n"
        f"⚖️ *Action:* `{action_taken.upper()}`\n"
        f"🗒️ *Reason:* `{reason}`\n"
        f"⚠️ *Total Strikes:* `{new_strike_count}`"
    )
    await log_to_admin_channel(context, log_message)

# --- Message & Command Handlers ---
async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for new and edited messages for crypto addresses."""
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    
    if not all([message, user, chat, message.text]): return
        
    try:
        member = await chat.get_member(user.id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]: return
    except Exception as e:
        logger.error(f"Could not check member status for {user.id} in {chat.id}: {e}")
        return

    if ADDRESS_REGEX.search(message.text):
        await process_spam(update, context, "Crypto Address Detected")
        
async def handle_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for messages containing links."""
    user = update.effective_user
    chat = update.effective_chat
    if not all([user, chat]): return
        
    try:
        member = await chat.get_member(user.id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]: return
    except Exception: return
        
    await process_spam(update, context, "Unauthorized Link")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to show statistics."""
    user = update.effective_user
    chat = update.effective_chat
    if not all([user, chat]): return
        
    try:
        member = await chat.get_member(user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            await update.message.reply_text("This command is for admins only.")
            return
    except Exception: return

    deleted, muted, banned = db.get_stats(chat.id)
    total_actions = deleted + muted + banned
    
    stats_text = (
        f"📈 *Bot Statistics for the Last 7 Days*\n\n"
        f"• Messages Deleted/Warned: `{deleted}`\n"
        f"• Users Muted: `{muted}`\n"
        f"• Users Banned: `{banned}`\n\n"
        f"Total actions taken: `{total_actions}`"
    )
    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN_V2)

# --- NEW: Handlers for Info Messages ---
async def info_handler_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the info message in a private chat."""
    await update.message.reply_text(SUPPORTED_CHAINS_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

async def info_handler_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the info message when the bot is mentioned in a group."""
    if context.bot.username in update.message.text:
        await update.message.reply_text(SUPPORTED_CHAINS_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

# --- Main Function to Run the Bot ---
def main():
    logger.info("Bot starting...")
    application = Application.builder().token(TOKEN).build()

    # --- Add Moderation Handlers ---
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), check_message))
    application.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE & filters.TEXT & (~filters.COMMAND), check_message))
    application.add_handler(MessageHandler(filters.Entity("url") | filters.Entity("text_link"), handle_links))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # --- Add NEW Info Handlers ---
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE, info_handler_private))
    application.add_handler(MessageHandler(filters.Entity("mention") & filters.ChatType.GROUP, info_handler_group))

    logger.info("Bot polling started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
