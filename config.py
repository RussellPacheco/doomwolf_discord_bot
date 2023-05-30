import configparser

class Config:
    def __init__(self):
        self._config = configparser.ConfigParser()
        files = self._config.read('doomwolf_bot.conf')
        if len(files) == 0 or len(self._config.sections()) == 0:
            open('doomwolf_bot.conf', 'w').close()
            self._config['GENERAL'] = {
                'Log_Level': 'INFO',
                'Enable_STDOut': 'True',
            }
            with open('doomwolf_bot.conf', 'w') as configfile:
                self._config.write(configfile)
            self._config.read('doomwolf_bot.conf')
        for section in self._config.sections():
            for key in self._config[section]:
                setattr(self, key, self._config[section][key]) 


config = Config()