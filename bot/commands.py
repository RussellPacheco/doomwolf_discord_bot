from main import BOT
from datetime import datetime
from common import Common


@BOT.command()
async def getallmessages(ctx):
    try:
        counter = 0

        async for message in ctx.history(limit=None):
            counter += 1

        await ctx.send(f"There are {counter - 2} previous messages.")

    except Exception as e:
        await ctx.send(f"Error: {e}")


@BOT.command()
async def getfirstmessage(ctx):
    try:
        first_message = await ctx.history(oldest_first=True, limit=2).flatten()

        await ctx.send(f"The first message ID is {first_message[0].id}")
        await ctx.send(f"The first message author is {first_message[0].author}")
        await ctx.send(f"The first message created_at is {first_message[0].created_at}")
        await ctx.send(f"The first message is {first_message[0].content}")

    except Exception as e:
        await ctx.send(e)


@BOT.command()
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


@BOT.command()
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


@BOT.command()
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


@BOT.command(name="getcommands", description="Returns all commands available")
async def getcommands(ctx):
    helptext = "```"
    for command in BOT.commands:
        helptext+=f"{command}\n"
    helptext += "```"
    await ctx.send(helptext)

@BOT.command()
async def deletionschedule(ctx):
    bot_login_times_file = open("bot_login_times.log", "r")
    bot_login_times = bot_login_times_file.readlines()
    latest_bot_login = bot_login_times[-1]

    deletion_times_files = open("deletion_times.log", "r")
    deletion_times = deletion_times_files.readlines()

    current_time = datetime.now()
    current_time = current_time.replace(microsecond=0)

    await ctx.send(f"This bot is scheduled to delete {Common.AMOUNT_TO_PASSIVE_DELETE} messages every {Common.AMOUNT_TIME} {Common.TIME}(s)")

    if len(deletion_times) > 0:
        latest_deletion = deletion_times[-1]
        latest_deletion = datetime.fromisoformat(latest_deletion)
        latest_deletion_plus_time = None

        if Common.TIME == "day":
            latest_deletion_plus_time = latest_deletion.replace(day=latest_deletion.day + Common.AMOUNT_TIME, microsecond=0)
        elif Common.TIME == "hour":
            latest_deletion_plus_time = latest_deletion.replace(hour=latest_deletion.hour + Common.AMOUNT_TIME, microsecond=0)
        elif Common.TIME == "minute":
            latest_deletion_plus_time = latest_deletion.replace(minute=latest_deletion.minute + Common.AMOUNT_TIME, microsecond=0)

        if latest_deletion_plus_time > current_time:
            await ctx.send(f"There is {latest_deletion_plus_time - current_time} left before the next deletion")

    else:
        latest_bot_login = datetime.fromisoformat(latest_bot_login)
        latest_bot_login_plus_time = None

        if Common.TIME == "day":
            latest_bot_login_plus_time = latest_bot_login.replace(day=latest_bot_login.day + Common.AMOUNT_TIME, microsecond=0)
        elif Common.TIME == "hour":
            latest_bot_login_plus_time = latest_bot_login.replace(hour=latest_bot_login.hour + Common.AMOUNT_TIME, microsecond=0)
        elif Common.TIME == "minute":
            latest_bot_login_plus_time = latest_bot_login.replace(minute=latest_bot_login.minute + Common.AMOUNT_TIME, microsecond=0)

        if latest_bot_login_plus_time > current_time:
            await ctx.send(f"There is {latest_bot_login_plus_time - current_time} left before the next deletion")


@BOT.command()
async def getmessagecount(ctx):
    file = open("message_ids.txt", "r")
    all_ids = file.readlines()
    total_messages = await ctx.history().flatten()

    file.close()

    await ctx.send(f"There are {len(all_ids)} message IDs registered in the database.")
    await ctx.send(f"There are {len(total_messages)} messages in the channel")
