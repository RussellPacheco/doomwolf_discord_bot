from bot import *
import os
from config import config

if __name__ == "__main__":
    if config.main_channel != "":
        if config.log_level == "DEBUG":
            BOT.run(os.environ.get("BOT_TOKEN"), log_handler=LOGGER.handler)
        else:
            BOT.run(os.environ.get("BOT_TOKEN"), log_handler=None)
    else:
        LOGGER.error("No main channel set in config.py. Exiting...")
        exit(1)
