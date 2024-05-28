import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'MTI0NDY4OTgyNTIxOTYxMjcyNA.G2Eo32.rsgIFyFEYUdoLK_l6MpaMDQWP5TRhNrxx2swhM'

# Replace with your specific channel IDs and role IDs
CHANNEL_IDS = [1241312294642913310, 1241312367019819029, 1241312413979250711, 1244631419578220545]  # List of channels to monitor
ROLE_IDS = [1241314877717483604, 1241315849047113788, 1241316000461357196, 1244639262994071553]  # Roles to check
LOG_CHANNEL_ID = 1241373360424751134  # Channel to log bot activities

# Google Sheets setup
SCOPE = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Use the path to your downloaded service account JSON file
# CREDS = ServiceAccountCredentials.from_json_keyfile_name('vigilant-result-424612-v9-0c357c5c6d9f.json', SCOPE)
CREDS = ServiceAccountCredentials.from_json_keyfile_name('roboticsclubapihandler-65e457d29ff9.json', SCOPE)
CLIENT = gspread.authorize(CREDS)

# Open the Google Sheet by name
# SHEET = CLIENT.open('Club_Status_Updates').sheet1
SHEET = CLIENT.open('DailyStatusUpdates').sheet1

# Define the intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent
intents.guilds = True
intents.members = True

# Create the bot instance with the defined intents
bot = commands.Bot(command_prefix='', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    await log_message(f'Bot started and logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.channel.id in CHANNEL_IDS:
        for role_id in ROLE_IDS:
            if discord.utils.get(message.author.roles, id=role_id):
                try:
                    save_message_to_google_sheets(message)
                    await log_message(f"Message from {message.author.nick or message.author.name} saved to Google Sheets.")
                except Exception as e:
                    await log_message(f"Error saving message from {message.author.nick or message.author.name}: {e}")
                break

async def log_message(content):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(content)

def save_message_to_google_sheets(message):
    # Get the user's nickname, or fall back to their username if no nickname is set
    user_nickname = message.author.nick or message.author.name
    data = [
        message.author.id,  # User ID
        user_nickname,  # User nickname
        message.content,  # Message content
        message.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Current date and time
    ]
    SHEET.append_row(data)  # Append the data as a new row in the Google Sheet

bot.run(TOKEN)
