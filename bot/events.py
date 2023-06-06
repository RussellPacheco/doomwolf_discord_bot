from main import BOT, LOGGER
from common import Common
from config import config
from db import db


@BOT.event
async def on_ready():
    channel = BOT.get_channel(config.main_channel)
    
    LOGGER.info('Bot has logged in as {0.user}'.format(BOT))
    LOGGER.info(f"Channel: {channel}")

    await channel.send(config.login_message)

@BOT.event
async def on_message(message):
    if message.author == BOT.user:
        return

    if message.content[0] == "$":
        if message.author.id == Common.BOBSANDERS_ID:
            await message.channel.send("Hey-o Bobby! You got a command for me? Right away, sir!")
        await BOT.process_commands(message)
