from dotenv import load_dotenv
import discord
from discord.ext import commands
from bot_logger import LOGGER


load_dotenv()
print("Starting everything")
####################
#
# Setup
#
####################

### DISCORD OPTIONS (guilds, messages, message_content must be True)
intents = discord.Intents.none()
intents.guilds = True
intents.messages = True
intents.message_content = True
description = "Let's vote on the next video theme!"

### Run zee bot!
LOGGER.info("Bot is running")
BOT = commands.Bot(command_prefix="$", description=description, intents=intents)

from .events import *
from .commands import *