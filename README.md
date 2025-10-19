# SpyCrypto Moderation Bot 🛡️

A powerful and intelligent Telegram moderation bot designed to keep your crypto-focused groups clean. It automatically detects and removes spammy messages, specializing in cryptocurrency wallet addresses and unauthorized links.

This bot uses a progressive 3-strike system to warn, mute, and finally ban persistent spammers, all while logging actions to a private admin channel.

## Features

* **Crypto Address Detection**: Automatically detects and removes messages containing wallet addresses from dozens of popular blockchains.
* **Link Removal**: Instantly deletes messages from new users that contain URLs or text links.
* **3-Strike System**: A progressive punishment system to handle offenders fairly but firmly.
* **Admin Whitelisting**: All group owners and administrators are automatically ignored by the spam filters.
* **Statistics**: An admin-only `/stats` command to see moderation actions over the last 7 days.
* **Private Logging**: Logs all actions (warnings, mutes, bans) to a designated admin channel for review.
* **Persistent Storage**: Uses MongoDB to track user strikes and log moderation history.

---

## How It Works: The 3-Strike System

The bot tracks offenses on a per-user, per-group basis.

1.  **Strike 1: Warn** ⚠️
    * The offending message is deleted.
    * The bot sends a public warning message, tagging the user.

2.  **Strike 2: Mute** 🔇
    * The offending message is deleted.
    * The user is muted in the group for **24 hours**.

3.  **Strike 3: Ban** 🚫
    * The offending message is deleted.
    * The user is **permanently banned** from the group.

---

## Supported Blockchains

The bot is powered by a comprehensive list of regex patterns to detect a wide variety of wallet addresses.

<details>
  <summary>Click to see the full list of detected chains</summary>
  
  * Algorand (ALGO)
  * Avalanche (AVAX X-Chain)
  * BNB Beacon Chain
  * Bitcoin (BTC)
  * Bitcoin Cash (BCH)
  * Cardano (ADA)
  * Cosmos (ATOM)
  * Dash (DASH)
  * Dogecoin (DOGE)
  * Ethereum (EVM chains)
  * Litecoin (LTC)
  * Monero (XMR)
  * NEAR Protocol
  * Polkadot (DOT)
  * Ripple (XRP)
  * Solana (SOL)
  * Stellar (XLM)
  * TRON (TRX)
  * Tezos (XTZ)
  * The Open Network (TON)
  * Zcash (ZEC)

</details>

---

## Bot Commands

### User Commands
* `/start` (in Private Chat): Shows the welcome message and the full list of supported chains.
* `@BotName` (in a Group): Mentioning the bot in a group will also trigger the info message.

### Admin-Only Commands
* `/stats`: Shows a 7-day summary of all actions taken by the bot in the current group (messages deleted, users muted, users banned).

---

## 🚀 Quick Start & Installation

You can run your own instance of this bot.

### 1. Prerequisites
* Python 3.8+
* A Telegram Bot Token from [@BotFather](https://t.me/BotFather)
* A MongoDB database (you can get a free one from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas))

### 2. Clone & Install
```bash
# Clone this repository
git clone [https://your-repo-url.git](https://your-repo-url.git)
cd spycrypto-bot

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

You will need a requirements.txt file:
python-telegram-bot
pymongo
python-dotenv
```
3. Configuration
Create a .env file in the main directory and fill it with your credentials:
# Get this from @BotFather
```
TELEGRAM_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
```
# Your MongoDB connection string
```
MONGO_URI="mongodb+srv://user:password@cluster0.abcde.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
```
### The chat ID of your private log channel (must start with -100)
### Make sure the bot is an admin in this channel!
```
ADMIN_LOG_CHANNEL="-1001234567890"
```
4. Run the Bot
```
python main.py
```
6. Add to Your Group
 * Add your bot to your Telegram group.
 * Promote it to Admin.
 * Grant it the following permissions:
   * Delete messages
   * Restrict users
   * Ban users
🤝 How to Contribute
We welcome contributions to make this bot even better! Whether it's adding a new blockchain regex, fixing a bug, or suggesting a new feature, your help is appreciated.
The easiest way to contribute is by adding new wallet address patterns!
If you want to contribute, please follow these steps:
 * Fork this repository.
 * Create a new branch for your feature or fix:
   git checkout -b feature/add-new-chain

 * Make your changes (e.g., add your new regex to the PATTERNS dictionary in main.py).
 * Commit your changes:
   git commit -m "feat: Add support for [Your Chain Name]"

 * Push to your branch:
   git push origin feature/add-new-chain

 * Open a Pull Request and describe your changes.
We'll review your PR as soon as possible. Thank you for helping keep Telegram crypto-safe!
