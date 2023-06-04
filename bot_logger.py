from config import config
import logging 

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('doomwolf_bot')
        numeric_level = getattr(logging, config.log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % config.log_level)
        logging.basicConfig(level=numeric_level)
        handler = logging.FileHandler(filename='doomwolf_bot.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s'))
        self.logger.addHandler(handler)
    def debug(self, message):
        if config.enable_stdout:
            print(f"DEBUG:{message}")
        self.logger.debug(message)
    def info(self, message):
        if config.enable_stdout:
            print(f"INFO:{message}")
        self.logger.info(message)
    def warning(self, message):
        if config.enable_stdout:
            print(f"WARNING:{message}")
        self.logger.warning(message)
    def error(self, message):
        if config.enable_stdout:
            print(f"ERROR:{message}")
        self.logger.error(message)


LOGGER = Logger()