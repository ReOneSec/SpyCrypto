<div align="center">
<img src="https://www.google.com/search?q=https://placehold.co/1200x400/0f172a/7dd3fc%3Ftext%3DSpyCrypto%26font%3Dmontserrat" alt="SpyCrypto Banner"/>
</div>
<div align="center">SpyCrypto - Advanced Telegram Moderator</div>
<div align="center">
<p>An intelligent, database-powered moderation bot to keep your Telegram groups clean from crypto spam, unauthorized links, and malicious content.</p>
</div>
<div align="center">
<!-- Badges -->
<a href="https://www.python.org/downloads/"><img src="https://www.google.com/search?q=https://img.shields.io/badge/Python-3.9%252B-blue%3Fstyle%3Dfor-the-badge%26logo%3Dpython%26logoColor%3Dwhite" alt="Python version"></a>
<a href="https://www.mongodb.com/cloud/atlas"><img src="https://www.google.com/search?q=https://img.shields.io/badge/MongoDB-Atlas-green%3Fstyle%3Dfor-the-badge%26logo%3Dmongodb%26logoColor%3Dwhite" alt="Database"></a>
<a href="#"><img src="https://www.google.com/search?q=https://img.shields.io/badge/Status-Active-brightgreen%3Fstyle%3Dfor-the-badge" alt="Project Status"></a>
<a href="LICENSE"><img src="https://www.google.com/search?q=https://img.shields.io/badge/License-MIT-purple%3Fstyle%3Dfor-the-badge" alt="License"></a>
</div>
<p align="center">See the bot in action. Real-time, detailed audit logs.</p>
<div align="center">
</div>
✨ Core Features
SpyCrypto is more than just a spam filter. It's a full moderation suite designed for modern community management.
| Icon | Feature | Description |
|---|---|---|
| 🛡️ | Multi-Chain Detection | Utilizes a comprehensive library of regex patterns to identify a vast range of crypto wallet addresses, preventing beggars and scammers. |
| ✍️ | Edited Message Scanning | Spammers can't evade the bot by editing their messages after posting. SpyCrypto re-scans all edited content to ensure nothing slips through. |
| ⚖️ | Progressive Strike System | Applies progressively severe punishments (Warn ➡️ Mute ➡️ Ban) for repeat offenders, ensuring fair moderation. Data is stored persistently in MongoDB. |
| 🔗 | Unauthorized Link Filtering | Automatically removes messages containing URLs or text links from non-admin users, a primary vector for scams and phishing attacks. |
| 👑 | Admin & Owner Immunity | Group administrators and the owner are completely ignored by the bot, allowing them to communicate and share important links freely without interference. |
| 📊 | On-Demand Statistics | Admins can get a quick report of the bot's moderation actions over the last 7 days directly in the chat using the /stats command. |
🔗 Supported Chains
To provide the best protection, SpyCrypto detects addresses from hundreds of blockchains. Here is a partial list of the most common ones.
<details>
<summary><strong>Click to view the full list of detectable chains</strong></summary>
EVM Chains (and hundreds more)
 * Ethereum (ETH)
 * BNB Smart Chain (BSC)
 * Polygon (MATIC)
 * Avalanche C-Chain (AVAX)
 * Fantom (FTM)
Bitcoin & Forks
 * Bitcoin (BTC) - Legacy & Bech32
 * Litecoin (LTC) - Legacy & Bech32
 * Dogecoin (DOGE)
 * Bitcoin Cash (BCH)
 * Dash (DASH)
 * Zcash (ZEC)
Major Alt-Chains
 * Solana (SOL)
 * TRON (TRX)
 * Polkadot (DOT)
 * Ripple (XRP)
 * Cardano (ADA) - Shelley & Byron
 * Monero (XMR)
 * Cosmos (ATOM)
 * Tezos (XTZ)
 * The Open Network (TON)
 * Stellar (XLM)
 * Algorand (ALGO)
 * NEAR Protocol
</details>
🚀 Getting Started: A 5-Minute Guide
Deploying your own instance of SpyCrypto is simple.
Step 1: Prerequisites
 * Python 3.9+
 * A MongoDB Atlas account (free tier is sufficient).
 * A Telegram Bot Token from @BotFather.
Step 2: Clone & Install
Clone the repository and install the required dependencies.
git clone <repository_url>
cd <repository_directory>
pip3 install -r requirements.txt

Step 3: Configure Your Bot
Create a .env file in the main directory and fill it with your credentials.
# --- Telegram Bot Configuration ---
# Get this token from @BotFather on Telegram.
TELEGRAM_TOKEN="YOUR_TELEGRAM_TOKEN_HERE"

# --- Database Configuration ---
# Get this from your MongoDB Atlas dashboard ("Connect your application").
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

# --- (Optional) Admin Logging ---
# The ID of the private channel for logs. Must start with a hyphen (-).
ADMIN_LOG_CHANNEL="-100123456789"

> 💡 Pro Tip: To get your ADMIN_LOG_CHANNEL ID, create a private channel, add the bot as an admin, send a message, and forward it to @userinfobot.
> 
Step 4: Launch the Bot
Run the bot from your terminal. For production, use a process manager like pm2 or screen.
python3 bot.py

Step 5: Final Group Setup
 * Add the Bot: Add your bot to the Telegram group you want to protect.
 * Promote to Admin: Make the bot an administrator with Delete messages, Ban users, and Restrict users permissions.
Your group is now protected! 🎉
🤖 Bot Commands
| Command | Description | Access |
|---|---|---|
| /stats | Shows a report of moderation actions in the last 7 days. | Admins only |
🙌 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.
If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement"
