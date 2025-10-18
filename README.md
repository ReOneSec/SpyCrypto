<div align="center">
<img src="https://www.google.com/search?q=https://placehold.co/1200x400/0f172a/7dd3fc%3Ftext%3DSpyCrypto%26font%3Dmontserrat" alt="SpyCrypto Banner"/>


<h1><strong>Advanced Telegram Crypto-Spam Moderator</strong></h1>
<p>An intelligent, database-powered moderation bot that keeps your Telegram groups clean from crypto spam, unauthorized links, and malicious content.</p>
<!-- Badges -->
<a href="https://www.python.org/downloads/"><img src="https://www.google.com/search?q=https://img.shields.io/badge/Python-3.9%252B-blue%3Fstyle%3Dflat-square%26logo%3Dpython%26logoColor%3Dwhite" alt="Python version"></a>
<a href="https://www.mongodb.com/cloud/atlas"><img src="https://www.google.com/search?q=https://img.shields.io/badge/MongoDB-Atlas-green%3Fstyle%3Dflat-square%26logo%3Dmongodb%26logoColor%3Dwhite" alt="Database"></a>
<a href="#"><img src="https://www.google.com/search?q=https://img.shields.io/badge/Status-Active-brightgreen%3Fstyle%3Dflat-square" alt="Project Status"></a>
<a href="LICENSE"><img src="https://www.google.com/search?q=https://img.shields.io/badge/License-MIT-purple%3Fstyle%3Dflat-square" alt="License"></a>
</div>
<p align="center">See the bot in action. Real-time, detailed audit logs.</p>
<div align="center">
┌─────────────────────────────────────────────────────────┐
│ 👁️ SpyCrypto Admin Logs                                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ✅ Action Taken in Crypto Traders Group                 │
│                                                         │
│ 👤 User: John Doe (12345678)                             │
│ ⚖️ Action: WARNED                                        │
│ 🗒️ Reason: Crypto Address Detected                      │
│ ⚠️ Total Strikes: 1                                     │
│ ------------------------------------------------------- │
│ ✅ Action Taken in Crypto Traders Group                 │
│                                                         │
│ 👤 User: Jane Smith (87654321)                           │
│ ⚖️ Action: MUTED                                         │
│ 🗒️ Reason: Unauthorized Link                           │
│ ⚠️ Total Strikes: 2                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘

</div>
✨ Why SpyCrypto?
Managing a crypto community is tough. You face a constant barrage of scammers, spammers, and malicious actors. SpyCrypto is your first line of defense, automating the tedious work of moderation so you can focus on building your community. It's fast, reliable, and smart.
<table width="100%">
<tr>
<td width="33%" align="center">
<img src="https://www.google.com/search?q=https://placehold.co/100x100/0f172a/7dd3fc%3Ftext%3D🛡️" alt="Shield Icon">
<h3>Intelligent Detection</h3>
<p>Goes beyond simple keywords to recognize dozens of blockchain address formats and link patterns.</p>
</td>
<td width="33%" align="center">
<img src="https://www.google.com/search?q=https://placehold.co/100x100/0f172a/7dd3fc%3Ftext%3D⚖️" alt="Scales Icon">
<h3>Fair Punishment System</h3>
<p>Uses a progressive strike system (Warn ➡️ Mute ➡️ Ban) to give users a chance while keeping the group safe.</p>
</td>
<td width="33%" align="center">
<img src="https://www.google.com/search?q=https://placehold.co/100x100/0f172a/7dd3fc%3Ftext%3D👑" alt="Crown Icon">
<h3>Admin-Aware</h3>
<p>Never interferes with admins or group owners, giving you complete freedom to manage your community.</p>
</td>
</tr>
</table>
🚀 Quick Start Guide
Deploying your own instance of SpyCrypto is simple and takes less than 5 minutes.
1. Prerequisites
 * Python 3.9+
 * A free MongoDB Atlas account.
 * A Telegram Bot Token from @BotFather.
2. Installation
# Clone the repository
git clone <repository_url>
cd <repository_directory>

# Install dependencies
pip3 install -r requirements.txt

3. Configuration
Create a .env file and populate it with your credentials.
# Telegram Bot Token from @BotFather
TELEGRAM_TOKEN="YOUR_TELEGRAM_TOKEN_HERE"

# MongoDB Connection String from Atlas
MONGO_URI="mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/"

# (Optional) Private channel ID for logs (must start with -100)
ADMIN_LOG_CHANNEL="-100123456789"

4. Launch
Run the bot. For production, use a process manager like pm2 or screen.
python3 bot.py

5. Final Group Setup
 * Add your bot to the target group.
 * Promote it to an Admin with Delete messages, Ban users, and Restrict users permissions.
Your group is now protected! 🎉
🤖 Bot Commands
The bot is designed to work silently in the background, but it has one essential command for admins.
| Command | Description | Access |
|---|---|---|
| /stats | Shows a report of moderation actions in the last 7 days. | Admins only |
🙌 Contributing
Contributions are welcome! If you have suggestions for new features, find a bug, or want to add more address patterns, please feel free to open an issue or submit a pull request.
📜 License
Distributed under the MIT License. See LICENSE for more information.
