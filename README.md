SpyCrypto - Advanced Telegram Crypto-Spam Moderation Bot
!(https://www.google.com/search?q=https://placehold.co/1200x300/4a5568/ffffff%3Ftext%3DSpyCrypto%2520Moderator)
SpyCrypto is a powerful and intelligent Telegram moderation bot designed to automatically detect and eliminate cryptocurrency spam from your groups. It goes beyond simple keyword filtering by using a configurable strike system, handling edited messages, filtering unauthorized links, and leveraging a persistent MongoDB database to track offenders.
This bot is perfect for community managers who want to maintain a clean, spam-free environment without constant manual intervention.
✨ Key Features
 * 🛡️ Multi-Chain Address Detection: Identifies a vast range of cryptocurrency wallet addresses across dozens of blockchains.
 * ✍️ Edited Message Scanning: Spammers can't evade the bot by editing their messages; SpyCrypto re-scans all edited content.
 * 🔗 Unauthorized Link Filtering: Automatically removes messages containing URLs or text links from non-admin users.
 * ⚖️ Configurable Strike System: Instead of an instant ban, the bot uses a multi-strike system:
   * Strike 1: Deletes the message and issues a public warning.
   * Strike 2: Deletes the message and mutes the user for 24 hours.
   * Strike 3: Deletes the message and permanently bans the user.
 * 👑 Admin-Aware: Group administrators and the owner are completely ignored by the bot, allowing them to post freely.
 * 📊 Statistics Command: Admins can use the /stats command to get a report of the bot's actions over the last 7 days.
 * ✍️ Audit Logging: All moderation actions are sent to a private admin channel, creating a clean and searchable audit log.
 * 💾 Persistent Memory: Uses a MongoDB database to remember user strike counts, ensuring that offenders are tracked across sessions.
🔗 Chains Supported
The bot can detect addresses from the following blockchains (and many more EVM-compatible chains):
|  |  |  |  |
|---|---|---|---|
| Ethereum (EVM) | Bitcoin (BTC) | Solana (SOL) | TRON (TRX) |
| Polkadot (DOT) | Dogecoin (DOGE) | Litecoin (LTC) | Ripple (XRP) |
| Cardano (ADA) | Monero (XMR) | BNB Chain (BNB) | Avalanche (AVAX) |
| Cosmos (ATOM) | Tezos (XTZ) | Dash (DASH) | Zcash (ZEC) |
| NEAR Protocol | Bitcoin Cash (BCH) | Stellar (XLM) | Algorand (ALGO) |
| The Open Network (TON) | and hundreds more... |  |  |
🚀 Setup and Installation
Follow these steps to deploy your own instance of the SpyCrypto bot.
1. Prerequisites
 * Python 3.9+ installed on your system or server.
 * A MongoDB Atlas account for the database. A free tier cluster is more than sufficient.
 * A Telegram Bot Token.
2. Clone the Repository
Clone this project to your local machine or server.
git clone <repository_url>
cd <repository_directory>

3. Install Dependencies
Install the required Python libraries using the requirements.txt file.
pip3 install -r requirements.txt

4. Configure the Bot
Create a file named .env in the project directory and copy the contents from the example below.
# --- Telegram Bot Configuration ---
# Get this token from @BotFather on Telegram.
TELEGRAM_TOKEN="123456:ABC-DeF12345ghIkl-zyx57W2v1uT0"

# --- Database Configuration ---
# Get this from your MongoDB Atlas dashboard (use the "Connect your application" option).
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

# --- (Optional) Admin Logging ---
# The ID of the private channel where the bot should send logs.
# Must start with a hyphen (-). Leave blank to disable.
ADMIN_LOG_CHANNEL=""

How to get the configuration values:
 * TELEGRAM_TOKEN: Talk to @BotFather on Telegram, create a new bot, and it will give you this token.
 * MONGO_URI:
   * Log in to your MongoDB Atlas account.
   * Create a free cluster.
   * In your cluster, go to Database Access and create a database user (e.g., spyCryptoBot) with a secure password.
   * Go to Network Access and add your server's IP address (or 0.0.0.0/0 for access from anywhere, less secure).
   * Go back to your cluster's Overview, click Connect, choose "Connect your application", and copy the connection string. Replace <username> and <password> with the credentials you created.
 * ADMIN_LOG_CHANNEL:
   * Create a private Telegram channel.
   * Add your bot to this channel as an administrator.
   * Forward any message from that channel to @userinfobot. It will reply with the channel's "Chat ID". Copy this ID (it will start with a -).
5. Run the Bot
Once configured, you can start the bot using:
python3 bot.py

It's recommended to run the bot in a screen session or using a process manager like pm2 or systemd to keep it online permanently.
🛠️ Usage in Your Group
 * Add the Bot: Add your bot to the Telegram group you want to protect.
 * Promote to Admin: Make the bot an administrator in your group. It needs the following permissions to function correctly:
   * Delete messages
   * Ban users
   * Restrict users
 * Check Statistics: As an admin, you can type /stats in the group to see a report of the bot's actions.
 * Monitor Logs: Keep an eye on your private log channel to see a real-time feed of all moderation actions.
This README was generated on Sunday, October 19, 2025.
