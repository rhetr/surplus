import os
import yaml

user_home = os.path.expanduser('~')

# from dataclasses import dataclass
# @dataclass
# class Config:
#     defaultDir: str
#     stylesheet: str
#     places: list[str]
#     recent: list[str]
#     play: bool
#     showWave: bool


class Config:
    def __init__(self):
        self.dir = self.initDir()
        self.stylesheet = os.path.join(self.dir, 'style.qss')
        self.path = os.path.join(self.dir, 'config.yml')
        self.defaults = self.loadDefaults()
        self.settings = self.loadSettings()

    def initDir(self) -> str:
        config_dir = os.path.join(
                os.getenv(
                    'XDG_CONFIG_HOME',
                    os.path.join(user_home, '.config')
                    ),
                'surplus'
                )
        if not os.path.isdir(config_dir):
            os.makedirs(config_dir)
        return config_dir

    def loadDefaults(self) -> dict:
        return {
                'Default Folder': user_home,
                'Stylesheet': self.stylesheet,
                'Places': [user_home],
                'Recent': [],
                'Play': True,
                'Show Waveform': True
                }

    def loadSettings(self) -> dict:
        if os.path.isfile(self.path):
            with open(self.path) as config_file:
                settings = yaml.safe_load(config_file)
            if self.validate(settings):
                return settings
        return self.createConfig()

    def createConfig(self) -> dict:
        print('making new config file')
        with open(self.path, 'w') as config_file:
            yaml.dump(self.defaults, config_file)
        return self.defaults

    def validate(self, settings: dict) -> bool:
        print('checking config..')
        if not (
                type(settings) is dict
                or all(
                    setting in settings.keys()
                    for setting in self.defaults.keys()
                    )
                ):
            badfile = f'{self.path}.bad'
            counter = 1
            while os.path.isfile(badfile + f'.{counter}'):
                counter += 1
            print(f'bad config. moving to {badfile}')
            os.rename(self.path, badfile + f'.{counter}')
            return False
        else:
            print('config ok')
            return True

    def updateRecent(self, path) -> None:
        if path in self.settings['Recent']:
            self.settings['Recent'].remove(path)
        self.settings['Recent'].append(path)
        if len(self.settings['Recent']) > 50:
            self.settings['Recent'].pop(0)

        self.save()

    # 1 = removed, 0 = added
    def modifyPlaces(self, path) -> int:
        if self.getPlacesIndex(path) == -1:
            result = 0
            self.settings['Places'].append(path)

        else:
            result = 1
            self.settings['Places'].remove(path)

        self.save()
        return result

    def getPlacesIndex(self, path) -> int:
        realpath = os.path.realpath(path)
        places = [os.path.realpath(sym) for sym in config.settings['Places']]
        if realpath in places:
            return places.index(realpath)
        else:
            return -1

    def update(self, key: str, value):
        pass

    def save(self) -> None:
        print('saving config')
        with open(self.path, 'w') as config_file:
            yaml.dump(self.settings, config_file)



config = Config()
