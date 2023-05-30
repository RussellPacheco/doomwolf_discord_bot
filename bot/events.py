from main import bot, logger
from utils import *
from common import Common

@bot.event
async def on_ready():
    channel = bot.get_channel(Common.BB_TEST_CHANNEL)
    # message = await channel.history().flatten()
    # if check_messages_for_deletion(message[0]):
    #     await delete_old_messages(channel)
    # await log_all_messages_id(channel)
    
    logger.info('Bot has logged in as {0.user}'.format(bot))
    logger.info(f"Channel: {channel}")

    await channel.send("Hey guys, any one up for some challenges?")


@bot.event
async def on_message(message):
    channel = bot.get_channel(Common.BB_TEST_CHANNEL)

    await log_all_messages_id(channel)

    if check_messages_for_deletion(message):
        await delete_old_messages(channel)

    if message.author == bot.user:
        return

    if message.author.id in Common.PERSONAL_ID_LIST and message.content[0] == "$":
        if message.author.id == Common.BOBSANDERS_ID:
            await message.channel.send("Hey-o Bobby! You got a command for me? Right away, sir!")
            await bot.process_commands(message)
        else:
            await message.channel.send(f"Hey there {message.author}. I'll take care of that for you.")
    elif message.content[0] == "$":
        await message.channel.send(f"Nice try @{message.author}, but this is a private bot only for God's hands.")
