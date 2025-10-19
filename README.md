md
# SpyCrypto

A Telegram bot that automatically deletes cryptocurrency wallet addresses from Telegram groups, helping to prevent scams and spam.

## Key Features & Benefits

*   **Automatic Wallet Address Detection:** Identifies and removes cryptocurrency wallet addresses shared in group chats.
*   **Spam Prevention:** Reduces crypto-related spam and phishing attempts.
*   **Group Security:** Enhances the overall security and safety of Telegram groups.
*   **Easy to Use:** Simple setup and configuration.

## Prerequisites & Dependencies

Before you begin, ensure you have the following installed:

*   **Python 3.6 or higher:**  Download from [python.org](https://www.python.org/downloads/)
*   **pip:** Python package installer (usually included with Python).
*   **Telegram Bot API Token:** Obtain from [BotFather](https://t.me/BotFather) on Telegram.
*   **MongoDB:** Ensure you have a MongoDB instance running.  Download from [mongodb.com](https://www.mongodb.com/try/download/community) or use a cloud-based service like MongoDB Atlas.

The following Python libraries are required:

*   `python-telegram-bot`
*   `python-dotenv`
*   `pymongo[srv]`

## Installation & Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ReOneSec/SpyCrypto.git
    cd SpyCrypto
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**

    *   Create a `.env` file in the project root directory.
    *   Add the following variables to the `.env` file, replacing the placeholders with your actual values:

        ```
        TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
        MONGODB_URI=YOUR_MONGODB_CONNECTION_STRING
        ```

    *   **TELEGRAM_BOT_TOKEN:** Your Telegram Bot API token obtained from BotFather.
    *   **MONGODB_URI:**  The connection string for your MongoDB database (e.g., `mongodb+srv://user:password@cluster.mongodb.net/database?retryWrites=true&w=majority`).

5.  **Run the bot:**

    ```bash
    python bot.py
    ```

## Usage Examples & API Documentation

Once the bot is running, add it to your Telegram group as an administrator. The bot will automatically detect and delete messages containing cryptocurrency wallet addresses.

**Commands (for bot admins):**

*   `/start` - Starts the bot and displays a welcome message. (Optional)

**Example (in a Telegram group):**

1.  User posts a message containing a cryptocurrency wallet address: "Check out my BTC wallet: bc1qxyz..."
2.  The bot automatically deletes the message.

## Configuration Options

The following environment variables can be configured in the `.env` file:

*   `TELEGRAM_BOT_TOKEN`:  The Telegram Bot API token.  (Required)
*   `MONGODB_URI`: The MongoDB connection string. (Required)
*   `LOG_LEVEL`:  Set the logging level (e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`).  Defaults to `INFO`.  Configure logging by changing level in `bot.py` if needed.
*   `ADMIN_USER_IDS`: A comma-separated list of Telegram user IDs who have admin privileges over the bot. (Optional, can be implemented in `bot.py`).

## Contributing Guidelines

We welcome contributions! To contribute to SpyCrypto, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes.
4.  Write tests to ensure your changes are working correctly.
5.  Submit a pull request.

Please ensure that your code adheres to the project's coding standards.

## License Information

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project uses the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library.
