import re
import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo import MongoClient

from telegram import Update, MessageEntity
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
# (This class is unchanged and correct)
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

    def reset_user_strikes(self, chat_id, user_id):
        result = self.strikes.delete_one({"chat_id": chat_id, "user_id": user_id})
        return result.deleted_count > 0

    def reset_all_strikes(self, chat_id):
        result = self.strikes.delete_many({"chat_id": chat_id})
        return result.deleted_count

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
        query = {"chat_id": chat_id, "timestamp": {"$gte": seven_days_ago}}
        deleted_count = self.actions.count_documents({**query, "action": "deleted"})
        muted_count = self.actions.count_documents({**query, "action": "muted"})
        banned_count = self.actions.count_documents({**query, "action": "banned"})
        return deleted_count, muted_count, banned_count

# --- Regex & Bot Data ---
PATTERNS = { "Ethereum (EVM chains)": r"0x[a-fA-F0-9]{40}", "Bitcoin (BTC)": r"[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-HJ-NP-Z0-9]{38,58}", "Litecoin (LTC)": r"[LM][a-km-zA-HJ-NP-Z1-9]{26,33}|ltc1[a-zA-HJ-NP-Z0-9]{39,59}", "Dogecoin (DOGE)": r"D[a-km-zA-HJ-NP-Z1-9]{33}", "Bitcoin Cash (BCH)": r"(bitcoincash:)?q[a-z0-9]{41}", "Dash (DASH)": r"X[1-9A-HJ-NP-Za-km-z]{33}", "Zcash (ZEC)": r"t1[a-km-zA-HJ-NP-Z1-9]{33}|z[a-km-zA-HJ-NP-Z1-9]{93}", "Solana (SOL)": r"[1-9A-HJ-NP-Za-km-z]{32,44}", "TRON (TRX)": r"T[a-zA-HJ-NP-Z1-9]{33}", "Polkadot (DOT)": r"1[a-zA-HJ-NP-Z1-9]{46,47}", "Ripple (XRP)": r"r[a-km-zA-HJ-NP-Z1-9]{25,34}", "Cardano (ADA)": r"addr1[a-z0-9]{98}|[DE][1-9A-HJ-NP-Za-km-z]{32,103}", "Monero (XMR)": r"4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}", "BNB Beacon Chain": r"bnb1[a-z0-9]{38}", "Avalanche (AVAX X-Chain)": r"X-[a-km-zA-HJ-NP-Z1-9]{44}", "Cosmos (ATOM)": r"cosmos1[a-z0-9]{38}", "Tezos (XTZ)": r"tz[1-3][a-km-zA-HJ-NP-Z1-9]{33}", "NEAR Protocol": r"[a-z0-9\._-]{2,64}\.near", "Stellar (XLM)": r"G[A-Z0-9]{55}", "Algorand (ALGO)": r"[A-Z2-7]{58}", "The Open Network (TON)": r"(?:-1|0):[a-fA-F0-9]{64}|[UEk][a-zA-Z0-9\-_]{47}" }
ADDRESS_REGEX = re.compile(rf"\b({'|'.join(PATTERNS.values())})\b", re.IGNORECASE)

db = DatabaseManager(MONGO_URI)

# --- Helper Functions ---
def escape_markdown_v2(text: str) -> str:
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

CHAIN_LIST_TEXT = "\n".join([f"• {escape_markdown_v2(name)}" for name in sorted(PATTERNS.keys())])
SUPPORTED_CHAINS_MESSAGE = (
    f"🛡️ *SpyCrypto Moderation Bot*\n\n"
    f"I keep groups clean by automatically detecting and removing spam\. "
    f"I scan new messages, edited messages, and links for unauthorized content\.\n\n"
    f"*I can detect addresses from hundreds of blockchains, including:*\n"
    f"{CHAIN_LIST_TEXT}"
)

# --- UPGRADED: Help message with clearer instructions ---
HELP_MESSAGE = (
    f"🛡️ *SpyCrypto Bot Help*\n\n"
    f"I am a moderation bot that keeps this group clean\. Here's how to use me:\n\n"
    f"*Everyone can use:*\n"
    f"`/help`: Shows this help message\.\n"
    f"`/start` \(in PM\): Shows supported chains\.\n"
    f"`@my_username` \(in group\): Mention me to see the list of supported chains\.\n\n"
    f"*Admin\-Only Commands:*\n"
    f"`/ping`: Check if I'm online and responsive\.\n"
    f"`/stats`: View spam statistics for the last 7 days\.\n"
    f"`/reset`: Reply to a user OR use their ID to reset their strikes to 0\.\n"
    f"  • *Usage \(Reply\):* Reply to a user's message with `/reset`\n"
    f"  • *Usage \(ID\):* Type `/reset 123456789`\n"
    f"`/resetall`: Reset the strike count for *all* members in this group\."
)

async def log_to_admin_channel(context: ContextTypes.DEFAULT_TYPE, message: str):
    if ADMIN_LOG_CHANNEL:
        try:
            await context.bot.send_message(chat_id=ADMIN_LOG_CHANNEL, text=message, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            logger.error(f"Failed to log to admin channel {ADMIN_LOG_CHANNEL}: {e}")

def get_user_mention(user):
    return user.mention_markdown_v2(user.full_name)

async def is_user_admin(chat, user_id):
    try:
        member = await chat.get_member(user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception as e:
        logger.error(f"Error checking admin status for {user_id} in {chat.id}: {e}")
        return False
    
# (process_spam, check_message, handle_links, stats_command, start_command, and info_handler_group are unchanged and correct)
# --- Core Logic: Punishment System ---
async def process_spam(update: Update, context: ContextTypes.DEFAULT_TYPE, reason: str):
    message, chat, user = update.effective_message, update.effective_chat, update.effective_user
    try: await message.delete()
    except (BadRequest, Forbidden): logger.warning(f"Could not delete message {message.message_id} in chat {chat.id}."); return
    new_strike_count = db.increment_user_strikes(chat.id, user.id, user.username or "N/A")
    user_mention, action_taken = get_user_mention(user), "deleted"
    if new_strike_count == 1:
        await context.bot.send_message(chat.id, f"{user_mention}, posting unauthorized content is not allowed\. This is your first warning\.", parse_mode=ParseMode.MARKDOWN_V2); action_taken = "warned"
    elif new_strike_count == 2:
        try:
            await context.bot.restrict_chat_member(chat.id, user.id, permissions={'can_send_messages': False}, until_date=datetime.now() + timedelta(days=1))
            await context.bot.send_message(chat.id, f"{user_mention}, you have received a second strike and are now muted for 24 hours\.", parse_mode=ParseMode.MARKDOWN_V2); action_taken = "muted"
        except (Forbidden, BadRequest): logger.warning(f"No permission to mute users in chat {chat.id}")
    else:
        try:
            await context.bot.ban_chat_member(chat.id, user.id)
            await context.bot.send_message(chat.id, f"{user_mention} has been banned after receiving three strikes\.", parse_mode=ParseMode.MARKDOWN_V2); action_taken = "banned"
        except (Forbidden, BadRequest): logger.warning(f"No permission to ban users in chat {chat.id}")
    db.log_action(chat.id, user.id, action_taken, reason)
    safe_reason, safe_chat_title = escape_markdown_v2(reason), escape_markdown_v2(chat.title)
    await log_to_admin_channel(context, f"✅ *Action Taken in {safe_chat_title}*\n\n👤 *User:* {user_mention} `({user.id})`\n⚖️ *Action:* `{escape_markdown_v2(action_taken.upper())}`\n🗒️ *Reason:* `{safe_reason}`\n⚠️ *Total Strikes:* `{new_strike_count}`")

# --- Message & Command Handlers ---
async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message, user, chat = update.effective_message, update.effective_user, update.effective_chat
    if not all([message, user, chat, message.text]): return
    if await is_user_admin(chat, user.id): return
    if ADDRESS_REGEX.search(message.text): await process_spam(update, context, "Crypto Address Detected")
        
async def handle_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user, chat = update.effective_user, update.effective_chat
    if not all([user, chat]): return
    if await is_user_admin(chat, user.id): return
    await process_spam(update, context, "Unauthorized Link")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user, chat = update.effective_user, update.effective_chat
    if not all([user, chat]): return
    if not await is_user_admin(chat, user.id): await update.message.reply_text("This command is for admins only."); return
    deleted, muted, banned = db.get_stats(chat.id)
    total_actions = deleted + muted + banned
    await update.message.reply_text(f"📈 *Bot Statistics for the Last 7 Days*\n\n• Messages Deleted/Warned: `{deleted}`\n• Users Muted: `{muted}`\n• Users Banned: `{banned}`\n\nTotal actions taken: `{total_actions}`", parse_mode=ParseMode.MARKDOWN_V2)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(SUPPORTED_CHAINS_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

async def info_handler_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot.username in update.message.text:
        await update.message.reply_text(SUPPORTED_CHAINS_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

# --- NEW: /ping command handler ---
async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """A simple command to check if the bot is alive."""
    await update.message.reply_text("Pong\! I am online and running\.", parse_mode=ParseMode.MARKDOWN_V2)

# --- NEW: /help command handler ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /help command."""
    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

# --- UPGRADED: A much more robust reset_user_command ---
async def reset_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to reset a single user's strikes."""
    admin_user, chat, message = update.effective_user, update.effective_chat, update.effective_message
    if not all([admin_user, chat]): return

    if not await is_user_admin(chat, admin_user.id):
        await update.message.reply_text("This command is for admins only.")
        return

    target_user_id = None
    target_user_mention = None

    # Case 1: Command is a reply
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
        target_user_id = target_user.id
        target_user_mention = get_user_mention(target_user)

    # Case 2: Command has a user ID as an argument
    elif context.args:
        try:
            target_user_id = int(context.args[0])
            # We don't know the user's name, so we create a simple mention
            target_user_mention = f"User with ID `{target_user_id}`"
        except (ValueError, IndexError):
            await update.message.reply_text("Invalid User ID provided\.", parse_mode=ParseMode.MARKDOWN_V2)
            return

    # If no target was found
    if not target_user_id:
        await update.message.reply_text(
            "Please reply to a user or provide their User ID to reset their strikes\.",
            parse_mode=ParseMode.MARKDOWN_V2
        )
        return
    
    # Perform the reset
    if db.reset_user_strikes(chat.id, target_user_id):
        reply_text = f"✅ Strikes for {target_user_mention} have been reset to 0\."
        
        # Log the action
        admin_mention = get_user_mention(admin_user)
        log_message = (
            f"ℹ️ *Moderation Action in {escape_markdown_v2(chat.title)}*\n\n"
            f"👤 *Target User:* {target_user_mention} `({target_user_id})`\n"
            f"⚖️ *Action:* `Strikes Reset`\n"
            f"👮 *Admin:* {admin_mention}"
        )
        await log_to_admin_channel(context, log_message)
    else:
        reply_text = f"This user \({target_user_mention}\) had no strikes to reset\."
        
    await update.message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

async def reset_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to reset all strikes in the group."""
    admin_user, chat = update.effective_user, update.effective_chat
    if not all([admin_user, chat]): return
    
    if not await is_user_admin(chat, admin_user.id):
        await update.message.reply_text("This command is for admins only."); return

    reset_count = db.reset_all_strikes(chat.id)
    reply_text = f"✅ All strikes have been reset\. {reset_count} user records were cleared\."
    
    admin_mention = get_user_mention(admin_user)
    log_message = (
        f"ℹ️ *Moderation Action in {escape_markdown_v2(chat.title)}*\n\n"
        f"⚖️ *Action:* `All Strikes Reset`\n"
        f"👮 *Admin:* {admin_mention}"
    )
    await log_to_admin_channel(context, log_message)
    
    await update.message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN_V2)

# --- Main Function to Run the Bot ---
def main():
    logger.info("Bot starting...")
    application = Application.builder().token(TOKEN).build()

    # Add Moderation Handlers
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), check_message))
    application.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE & filters.TEXT & (~filters.COMMAND), check_message))
    application.add_handler(MessageHandler(filters.Entity("url") | filters.Entity("text_link"), handle_links))
    
    # Add Command Handlers
    application.add_handler(CommandHandler("start", start_command, filters=filters.ChatType.PRIVATE))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping_command)) # NEW
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("reset", reset_user_command, filters=filters.ChatType.GROUP))
    application.add_handler(CommandHandler("resetall", reset_all_command, filters=filters.ChatType.GROUP))
    
    # Add Info Handlers
    application.add_handler(MessageHandler(filters.Entity("mention") & filters.ChatType.GROUP, info_handler_group))

    logger.info("Bot polling started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
    
