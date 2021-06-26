from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging
from datetime import datetime
import os

load_dotenv()

####################
#
#     Channels
#
####################

OFF_TOPIC_CHANNEL = 824643646748885022
BB_GENERAL_CHANNEL = 711441407914672162
BB_TEST_CHANNEL = 858188090610155530
BOBSANDERS_TEST_SERVER_GENERAL_CHANNEL = 857208225974452247


####################
#
# Allowed Users
#
####################

BOBSANDERS_ID = 636913307605008407
PERSONAL_ID_LIST = [BOBSANDERS_ID, ]

####################
#
# Passive Deletion Time Config
#
####################

TIME = "day"  # "day", "hour", or "minute"
AMOUNT_TIME = 1
AMOUNT_TO_PASSIVE_DELETE = 24 #how many messages to passively delete.


####################
#
# Setup
#
####################


#### LOGGER
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord_debug.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


### DISCORD
intents = discord.Intents.default()
intents.members = True
description = "A bot for deleting old messages!"

bot = commands.Bot(command_prefix="$", description=description, intents=intents)


####################
#
#  Util Functions
#
####################

def log_login():
    file = open("bot_login_times.log", "a")

    file.write(f"\n{datetime.now()}")
    file.close()

    print(f"Bot has logged in at <{datetime.now()}>")


async def log_all_messages_id(channel):
    all_messages = await channel.history(limit=None, oldest_first=True).flatten()
    file = open("message_ids.txt", "w")

    for message in all_messages:
        file.write(str(message.id) + "\n")

    file.close()


def check_messages_for_deletion(message):
    if message.channel.id == BB_TEST_CHANNEL:

        file = open("deletion_times.log", "a")
        file.close()

        login_times_file = open("bot_login_times.log", "r")
        deletion_times_file = open("deletion_times.log", "r")
        deletion_times = deletion_times_file.readlines()
        
        current_time = datetime.now()
        login_times_file_data = login_times_file.readlines()
        login_times_file_length = len(login_times_file_data)

        if login_times_file_length > 0:
            if len(deletion_times) > 0:
                last_deletion_unparsed = deletion_times[-1]
                last_deletion = datetime.fromisoformat(last_deletion_unparsed)
                last_deletion_plus_time = None

                if TIME == "day":
                    print("I went to day")
                    last_deletion_plus_time = last_deletion.replace(day=last_deletion.day + AMOUNT_TIME)
                elif TIME == "hour":
                    print("I went to hour")
                    last_deletion_plus_time = last_deletion.replace(hour=last_deletion.hour + AMOUNT_TIME / 60)
                elif TIME == "minute":
                    print("I went to minute")
                    print(f"{last_deletion.minute}")
                    last_deletion_plus_time = last_deletion.replace(minute=last_deletion.minute + AMOUNT_TIME % 60)

                deletion_times_file.close()

                if last_deletion_plus_time <= current_time:
                    return True
                else:
                    return False

            else:
                last_login_time_unparsed = login_times_file_data[-1]
                last_login_time = datetime.fromisoformat(last_login_time_unparsed)
                last_login_time_plus_time = None

                if TIME == "day":
                    last_login_time_plus_time = last_login_time.replace(day=last_login_time.day + AMOUNT_TIME)
                elif TIME == "hour":
                    last_login_time_plus_time = last_login_time.replace(hour=last_login_time.hour + AMOUNT_TIME)
                elif TIME == "minute":
                    last_login_time_plus_time = last_login_time.replace(minute=last_login_time.minute + AMOUNT_TIME)

                login_times_file.close()

                if last_login_time_plus_time <= current_time:
                    return True
                else:
                    return False
        else:
            return False


async def delete_old_messages(channel):

    file = open("message_ids.txt", "a")
    file.close()

    file = open("message_ids.txt", "r")
    all_saved_ids = file.readlines()
    file.close()

    counter = 0

    while counter != AMOUNT_TO_PASSIVE_DELETE and len(all_saved_ids) > 0:
        for number in range(AMOUNT_TO_PASSIVE_DELETE):
            message = await channel.fetch_message(all_saved_ids[number])
            await channel.send(f"I am deleting {message.content} by {message.author} made on {message.created_at}.")
            await message.delete()
            all_saved_ids.remove(all_saved_ids[number])
            counter += 1

    file = open("message_ids.txt", "w")

    for line in all_saved_ids:
        file.write(line)

    file.close()

    file = open("deletion_times.log", "r")
    past_deletion_times = file.readlines()
    file.close()

    file = open("deletion_times.log", "w")

    for times in past_deletion_times:
        file.write(times + "\n")

    file.write(f"{datetime.now()}")

    file.close()

    await log_all_messages_id(channel)

####################
#
#     Events
#
####################


@bot.event
async def on_ready():
    channel = bot.get_channel(BB_TEST_CHANNEL)

    message = await channel.history().flatten()
    if check_messages_for_deletion(message[0]):
        await delete_old_messages(channel)

    log_login()
    await log_all_messages_id(channel)

    print('We have logged in as {0.user}'.format(bot))
    print(f"The channel I am focusing on is {channel}")

    await channel.send("Hey guys, I'm new!")


@bot.event
async def on_message(message):
    channel = bot.get_channel(BB_TEST_CHANNEL)

    await log_all_messages_id(channel)

    if check_messages_for_deletion(message):
        await delete_old_messages(channel)

    if message.author == bot.user:
        return

    if message.author.id in PERSONAL_ID_LIST and message.content[0] == "$":
        if message.author.id == BOBSANDERS_ID:
            await message.channel.send("Hey-o Bobby! You got a command for me? Right away, sir!")
            await bot.process_commands(message)
        else:
            await message.channel.send(f"Hey there {message.author}. I'll take care of that for you.")
    elif message.content[0] == "$":
        await message.channel.send(f"Nice try @{message.author}, but this is a private bot only for God's hands.")


@bot.command()
async def getallmessages(ctx):
    try:
        counter = 0

        async for message in ctx.history(limit=None):
            counter += 1

        await ctx.send(f"There are {counter - 2} previous messages.")

    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command()
async def getfirstmessage(ctx):
    try:
        first_message = await ctx.history(oldest_first=True, limit=2).flatten()

        await ctx.send(f"The first message ID is {first_message[0].id}")
        await ctx.send(f"The first message author is {first_message[0].author}")
        await ctx.send(f"The first message created_at is {first_message[0].created_at}")
        await ctx.send(f"The first message is {first_message[0].content}")

    except Exception as e:
        await ctx.send(e)


@bot.command()
async def deletemsg(ctx, id):
    try:
        message_to_delete = await ctx.fetch_message(id)
        created_at = message_to_delete.created_at
        content = message_to_delete.content
        author = message_to_delete.author

        await message_to_delete.delete()
        await ctx.send(f"Deleted {content}. Created At: {created_at}. Author: {author}")
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command()
async def deleteallmsgs(ctx):
    try:
        all_messages = await ctx.history().flatten()

        await ctx.send(f"I will delete {len(all_messages)} messages now.")

        counter = 0
        for message in all_messages:
            counter += 1
            await message.delete()

        await ctx.send(f"I deleted {counter} message(s)")
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command()
async def deletefirst(ctx, num):
    try:
        first_n_msgs = await ctx.history(limit=int(num), oldest_first=True).flatten()

        await ctx.send(f"I will be deleting the first {len(first_n_msgs)} msg(s).")

        counter = 0

        for message in first_n_msgs:
            counter += 1
            await ctx.send(f"{counter}: Deleted {message.content} posted by {message.author} on {message.created_at}")
            await message.delete()

        await ctx.send(f"Deleted {counter} msg(s).")
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command(name="getcommands", description="Returns all commands available")
async def getcommands(ctx):
    helptext = "```"
    for command in bot.commands:
        helptext+=f"{command}\n"
    helptext += "```"
    await ctx.send(helptext)

@bot.command()
async def deletionschedule(ctx):
    bot_login_times_file = open("bot_login_times.log", "r")
    bot_login_times = bot_login_times_file.readlines()
    latest_bot_login = bot_login_times[-1]

    deletion_times_files = open("deletion_times.log", "r")
    deletion_times = deletion_times_files.readlines()

    current_time = datetime.now()
    current_time = current_time.replace(microsecond=0)

    await ctx.send(f"This bot is scheduled to delete {AMOUNT_TO_PASSIVE_DELETE} messages every {AMOUNT_TIME} {TIME}(s)")

    if len(deletion_times) > 0:
        latest_deletion = deletion_times[-1]
        latest_deletion = datetime.fromisoformat(latest_deletion)
        latest_deletion_plus_time = None

        if TIME == "day":
            latest_deletion_plus_time = latest_deletion.replace(day=latest_deletion.day + AMOUNT_TIME, microsecond=0)
        elif TIME == "hour":
            latest_deletion_plus_time = latest_deletion.replace(hour=latest_deletion.hour + AMOUNT_TIME, microsecond=0)
        elif TIME == "minute":
            latest_deletion_plus_time = latest_deletion.replace(minute=latest_deletion.minute + AMOUNT_TIME, microsecond=0)

        if latest_deletion_plus_time > current_time:
            await ctx.send(f"There is {latest_deletion_plus_time - current_time} left before the next deletion")

    else:
        latest_bot_login = datetime.fromisoformat(latest_bot_login)
        latest_bot_login_plus_time = None

        if TIME == "day":
            latest_bot_login_plus_time = latest_bot_login.replace(day=latest_bot_login.day + AMOUNT_TIME, microsecond=0)
        elif TIME == "hour":
            latest_bot_login_plus_time = latest_bot_login.replace(hour=latest_bot_login.hour + AMOUNT_TIME, microsecond=0)
        elif TIME == "minute":
            latest_bot_login_plus_time = latest_bot_login.replace(minute=latest_bot_login.minute + AMOUNT_TIME, microsecond=0)

        if latest_bot_login_plus_time > current_time:
            await ctx.send(f"There is {latest_bot_login_plus_time - current_time} left before the next deletion")


@bot.command()
async def getmessagecount(ctx):
    file = open("message_ids.txt", "r")
    all_ids = file.readlines()
    total_messages = await ctx.history().flatten()

    file.close()

    await ctx.send(f"There are {len(all_ids)} message IDs registered in the database.")
    await ctx.send(f"There are {len(total_messages)} messages in the channel")


bot.run(os.getenv("BOT_TOKEN"))