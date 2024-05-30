import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
import os
import json

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix=None, intents=intents)
load_dotenv()

# Load environment variables
google_service_account_data = json.loads(os.getenv('GOOGLE_SERVICE_ACCOUNT_DATA'))

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets", 
         "https://www.googleapis.com/auth/drive.file", 
         "https://www.googleapis.com/auth/drive"]


creds = ServiceAccountCredentials.from_json_keyfile_dict(google_service_account_data, scope)
client = gspread.authorize(creds)
sheet = client.open("statusupdates").sheet1

# Define roles and channels to log
ROLES_TO_LOG       = [1241314877717483604, 1241315849047113788, 1241316000461357196, 1244639262994071553, 1245619973766774784]  # replace with your role IDs
CHANNELS_TO_LOG    = [1241312294642913310, 1241312367019819029, 1241312413979250711, 1244631419578220545, 1245619149917388881]  # replace with your channel IDs
LOGGING_CHANNEL_ID = 1241373360424751134  # replace with your logging channel ID

# Emojis for reactions
GREEN_TICK = '✅'
RED_CROSS = '❌'

@bot.event
async def on_ready():
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f'Bot connected as {bot.user}')
    print('Bot connected')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Check if the message is in the specified channels and the user has the specified roles
    if message.channel.id in CHANNELS_TO_LOG and any(role.id in ROLES_TO_LOG for role in message.author.roles):
        username = str(message.author.nick or message.author.name)
        ist = pytz.timezone('Asia/Kolkata')
        timestamp = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
        content = message.content
        
        try:
            # Append data to Google Sheet
            sheet.append_row([username, timestamp, content])
            
            # Send a log message to the logging channel
            log_channel = bot.get_channel(LOGGING_CHANNEL_ID)
            if log_channel:
                log_message = f"Logged message from {username} in [{message.channel.name}](https://discord.com/channels/{message.guild.id}/{message.channel.id}) at {timestamp}"
                await log_channel.send(log_message)
            
            # Add a green tick reaction to indicate successful saving
            await message.add_reaction(GREEN_TICK)
        except Exception as e:
            # Send a log message to the logging channel if saving failed
            if log_channel:
                await log_channel.send(f"Failed to log message from {username} in {message.channel.name}: {e}")
            
            # Add a red cross reaction to indicate failed saving
            await message.add_reaction(RED_CROSS)

# Run the bot
discord_token = os.getenv('DISCORD_TOKEN')
bot.run(discord_token)
