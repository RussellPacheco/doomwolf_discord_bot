from main import BOT, LOGGER
from common import Common

@BOT.event
async def on_ready():
    channel = BOT.get_channel(Common.BOBSANDERS_TEST_SERVER_GENERAL_CHANNEL)
    # message = await channel.history().flatten()
    # if check_messages_for_deletion(message[0]):
    #     await delete_old_messages(channel)
    # await log_all_messages_id(channel)
    
    LOGGER.info('BOT has logged in as {0.user}'.format(BOT))
    LOGGER.info(f"Channel: {channel}")

    await channel.send("Hey guys, any one up for some challenges?")


@BOT.event
async def on_message(message):
    print(f"Message: {message.content}")

    if message.author == BOT.user:
        return

    if message.author.id in Common.PERSONAL_ID_LIST and message.content[0] == "$":
        if message.author.id == Common.BOBSANDERS_ID:
            print("Author was BobSanders")
            await message.channel.send("Hey-o Bobby! You got a command for me? Right away, sir!")
            await BOT.process_commands(message)
        else:
            await message.channel.send(f"Hey there {message.author}. I'll take care of that for you.")
    elif message.content[0] == "$":
        await message.channel.send(f"Nice try @{message.author}, but this is a private bot only for God's hands.")