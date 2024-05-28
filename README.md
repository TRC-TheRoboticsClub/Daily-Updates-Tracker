
# Discord Bot for Logging Messages to Google Sheets

This Discord bot monitors specific channels for messages from users with certain roles and saves the message details to a Google Sheet for logging and analysis. It securely accesses the Google Sheets API and logs its activities to a designated Discord channel.

## Features

- Tracks messages in specified channels from users with certain roles.
- Saves message details, including user ID, nickname, content, and timestamp, to a Google Sheet.
- Logs bot activities and errors to a designated Discord channel.

## Setup

### Prerequisites

- Python 3.6 or higher
- Discord bot token
- Google Service Account credentials JSON file

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
   ```
2. Create and activate a virtual environment (optional but recommended):

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```
4. Set up your environment variables for the bot token and Google credentials JSON file path:

   ```sh
   export DISCORD_BOT_TOKEN='your_bot_token'
   export GOOGLE_CREDS_JSON_PATH='path/to/your/credentials.json'
   ```

### Configuration

- Update `CHANNEL_IDS`, `ROLE_IDS`, and `LOG_CHANNEL_ID` in the script to match your Discord server's configuration.
- Ensure your Google Sheets document is set up and accessible via the provided credentials.

### Running the Bot

Run the bot using the following command:

```sh
python bot.py
```

## Usage

- The bot will automatically log messages from specified channels and users with certain roles to the configured Google Sheet.
- It will also log its activities to the specified Discord channel.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Replace placeholders like `yourusername` and `your-repository` with your actual GitHub username and repository name. Save this content to a `README.md` file in your project directory.
