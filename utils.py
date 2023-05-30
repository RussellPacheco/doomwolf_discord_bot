from main import config, logger
import datetime
from common import Common

async def log_all_messages_id(channel):
    all_messages = await channel.history(limit=None, oldest_first=True).flatten()
    file = open("message_ids.txt", "w")

    for message in all_messages:
        file.write(str(message.id) + "\n")

    file.close()


def check_messages_for_deletion(message):
    if message.channel.id == Common.BB_TEST_CHANNEL:

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

                if Common.TIME == "day":
                    print("I went to day")
                    last_deletion_plus_time = last_deletion.replace(day=last_deletion.day + Common.AMOUNT_TIME)
                elif Common.TIME == "hour":
                    print("I went to hour")
                    last_deletion_plus_time = last_deletion.replace(hour=last_deletion.hour + Common.AMOUNT_TIME / 60)
                elif Common.TIME == "minute":
                    print("I went to minute")
                    print(f"{last_deletion.minute}")
                    last_deletion_plus_time = last_deletion.replace(minute=last_deletion.minute + Common.AMOUNT_TIME % 60)

                deletion_times_file.close()

                if last_deletion_plus_time <= current_time:
                    return True
                else:
                    return False

            else:
                last_login_time_unparsed = login_times_file_data[-1]
                last_login_time = datetime.fromisoformat(last_login_time_unparsed)
                last_login_time_plus_time = None

                if Common.TIME == "day":
                    last_login_time_plus_time = last_login_time.replace(day=last_login_time.day + Common.AMOUNT_TIME)
                elif Common.TIME == "hour":
                    last_login_time_plus_time = last_login_time.replace(hour=last_login_time.hour + Common.AMOUNT_TIME)
                elif Common.TIME == "minute":
                    last_login_time_plus_time = last_login_time.replace(minute=last_login_time.minute + Common.AMOUNT_TIME)

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

    while counter != Common.AMOUNT_TO_PASSIVE_DELETE and len(all_saved_ids) > 0:
        for number in range(Common.AMOUNT_TO_PASSIVE_DELETE):
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
