<div align="center">
<img src="https://www.google.com/search?q=https://placehold.co/1200x400/1e293b/94a3b8%3Ftext%3DSpyCrypto%250AAdvanced%2520Telegram%2520Moderator%26font%3Dmontserrat" alt="SpyCrypto Banner">
<h1>SpyCrypto - Advanced Telegram Crypto-Spam Moderator</h1>
<p>
An intelligent, database-powered moderation bot to keep your Telegram groups clean from crypto spam, unauthorized links, and malicious content.
</p>
<p>
<a href="https://www.python.org/downloads/"><img src="https://www.google.com/search?q=https://img.shields.io/badge/python-3.9%252B-3776AB%3Fstyle%3Dfor-the-badge%26logo%3Dpython" alt="Python version"></a>
<a href="https://www.mongodb.com/cloud/atlas"><img src="https://www.google.com/search?q=https://img.shields.io/badge/database-MongoDB-4EA94B%3Fstyle%3Dfor-the-badge%26logo%3Dmongodb" alt="Database"></a>
<a href="#"><img src="https://www.google.com/search?q=https://img.shields.io/badge/status-active-success%3Fstyle%3Dfor-the-badge" alt="Project Status"></a>
<a href="https://www.google.com/search?q=LICENSE"><img src="https://www.google.com/search?q=https://img.shields.io/badge/license-MIT-blue%3Fstyle%3Dfor-the-badge" alt="License"></a>
</p>
</div>
SpyCrypto is a powerful moderation bot designed to automatically detect and eliminate cryptocurrency spam from your groups. It goes beyond simple keyword filtering by using a configurable strike system, handling edited messages, filtering unauthorized links, and leveraging a persistent MongoDB database to track offenders.
This bot is perfect for community managers who want to maintain a clean, spam-free environment without constant manual intervention.
📖 Table of Contents
 * How It Works
 * Key Features
 * Chains Supported
 * Setup and Installation
 * Usage in Your Group
 * Bot Commands
 * Contributing
 * License
⚙️ How It Works
The bot follows a logical flow for every message it sees, ensuring fair and accurate moderation.
 * Message Received: A new message is posted or an existing one is edited.
 * Admin Check: The bot checks if the author is a group admin or owner. If so, the message is ignored.
 * Content Analysis: The message is scanned for violations:
   * Cryptocurrency addresses.
   * URLs or text links.
 * Violation Found:
   * The offending message is immediately deleted.
   * The user's strike count is retrieved from the MongoDB database.
 * Action Taken: Based on the new strike count, the bot applies a punishment (Warn, Mute, or Ban).
 * Logging: A detailed log of the action is sent to the private admin channel.
✨ Key Features
| Feature | Description |
|---|---|
| 🛡️ Multi-Chain Detection | Identifies a vast range of crypto wallet addresses across dozens of blockchains. |
| ✍️ Edited Message Scanning | Spammers can't evade the bot by editing their messages; SpyCrypto re-scans all edited content. |
| 🔗 Link Filtering | Automatically removes messages containing URLs or text links from non-admin users. |
| ⚖️ Strike System | Applies progressively severe punishments (Warn -> Mute -> Ban) for repeat offenders. |
| 👑 Admin-Aware | Group administrators and the owner are completely ignored by the bot, allowing them to post freely. |
| 📊 Statistics Command | Admins can get a report of the bot's actions over the last 7 days using the /stats command. |
| ✍️ Audit Logging | All moderation actions are sent to a private admin channel, creating a clean and searchable audit log. |
| 💾 Persistent Memory | Uses a MongoDB database to remember user strike counts, ensuring that offenders are tracked across server restarts. |
🔗 Chains Supported
The bot can detect addresses from the following blockchains (and hundreds more EVM-compatible chains):
|  |  |  |  |
|---|---|---|---|
| Ethereum (EVM) | Bitcoin (BTC) | Solana (SOL) | TRON (TRX) |
| Polkadot (DOT) | Dogecoin (DOGE) | Litecoin (LTC) | Ripple (XRP) |
| Cardano (ADA) | Monero (XMR) | BNB Chain (BNB) | Avalanche (AVAX) |
| Cosmos (ATOM) | Tezos (XTZ) | Dash (DASH) | Zcash (ZEC) |
| NEAR Protocol | Bitcoin Cash (BCH) | Stellar (XLM) | Algorand (ALGO) |
| The Open Network (TON) | and hundreds more... |  |  |
🚀 Setup and Installation
1. Prerequisites
 * Python 3.9+
 * A MongoDB Atlas account (free tier is sufficient).
 * A Telegram Bot Token.
2. Clone the Repository
git clone <repository_url>
cd <repository_directory>

3. Install Dependencies
pip3 install -r requirements.txt

4. Configure the Bot
Create a .env file in the project directory and fill it with your credentials.
# --- Telegram Bot Configuration ---
# Get this token from @BotFather on Telegram.
TELEGRAM_TOKEN="YOUR_TELEGRAM_TOKEN_HERE"

# --- Database Configuration ---
# Get this from your MongoDB Atlas dashboard.
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

# --- (Optional) Admin Logging ---
# The ID of the private channel for logs. Must start with a hyphen (-).
ADMIN_LOG_CHANNEL=""

> 💡 Tip: To get your ADMIN_LOG_CHANNEL ID, create a private channel, add your bot as an admin, send a message, and forward it to @userinfobot.
> 
5. Run the Bot
python3 bot.py

It's highly recommended to run the bot in a screen session or using a process manager like pm2 or systemd to ensure it stays online.
🛠️ Usage in Your Group
 * Add the Bot: Add your bot to the Telegram group you want to protect.
 * Promote to Admin: Make the bot an administrator with the following permissions:
   * Delete messages
   * Ban users
   * Restrict users
 * Monitor Logs: Keep an eye on your private log channel to see a real-time feed of all moderation actions.
🤖 Bot Commands
| Command | Description | Access |
|---|---|---|
| /stats | Shows a report of moderation actions in the last 7 days. | Admins only |
🙌 Contributing
Contributions are welcome! If you have suggestions for new features, find a bug, or want to add more address patterns, please feel free to open an issue or submit a pull request.
