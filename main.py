from dotenv import load_dotenv
import discord
from discord.ext import commands
import os, configparser
from bot_logger import Logger
from config import Config
from bot_logger import LOGGER

load_dotenv()

####################
#
# Setup
#
####################

### DISCORD OPTIONS
intents = discord.Intents.default()
intents.members = True
intents.guild_messages = True
description = "Let's vote on the next video theme!"

### Run zee bot!
LOGGER.info("Bot is running")
BOT = commands.Bot(command_prefix="$", description=description, intents=intents)
import bot.events, bot.commands
BOT.run(os.getenv("BOT_TOKEN"))
