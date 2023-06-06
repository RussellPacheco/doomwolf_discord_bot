import configparser

class Config:
    def __init__(self):
        self._config = configparser.ConfigParser()
        files = self._config.read('discord_bot.conf')
        if len(files) == 0 or len(self._config.sections()) == 0:
            open('discord_bot.conf', 'w').close()
            self._config['GENERAL'] = {
                'log_level': 'INFO',
                'enable_stdout': 'True',
                'db_file_path': 'db/discord_bot.db',
                'login_message': 'oh hi, mark.'
            }
            self._config['CHANNELS'] = {
                'main_channel': '',
                'challenge_channel': '',
            }
            with open('discord_bot.conf', 'w') as configfile:
                self._config.write(configfile)
            self._config.read('discord_bot.conf')
        for section in self._config.sections():
            for key in self._config[section]:
                try:
                    new_value = int(self._config[section][key])
                    setattr(self, key, new_value)
                except ValueError:
                    setattr(self, key, self._config[section][key]) 


config = Config()