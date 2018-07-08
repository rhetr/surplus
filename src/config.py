#!/usr/bin/env python3
'''
config.py is the configuration script for surplus
'''

import os
import yaml
import time

config_folder = os.path.expanduser('~') + '/.config/surplus/'
if not os.path.isdir(config_folder): os.makedirs(config_folder)
config_file = config_folder + 'config'

config_default = {
        'Default Folder': os.path.expanduser('~'),
        'Stylesheet': os.path.join(config_folder, 'style.qss'),
        'Places': [os.path.expanduser('~')],
        'Recent': [],
        'Play': True,
        'Show Waveform': True
        }

def make_config_file(config_file, config):
    print('making new config file')
    with open(config_file, 'w') as config_file_settings:
        yaml.dump(config_default, config_file_settings)

def check_config(config):
    print('checking config..')
    if not (type(config) == dict) \
            or not all(setting in config.keys() \
            for setting in config_default.keys()):
        badfile = config_file + '.bad.' + str(int(time.time()))
        print('bad config. moving to {}'.format(badfile))
        os.rename(config_file, badfile)
        raise TypeError
    else:
        print('config ok')

try:
    with open(config_file, 'rb') as config_file_settings:
        config = yaml.load(config_file_settings)
        check_config(config)
except (FileNotFoundError, TypeError) as e:
    print(e)
    make_config_file(config_file, config_default)
    config = config_default
