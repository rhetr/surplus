#!/usr/bin/env python3
'''
config.py is the configuration script for surplus
'''

import os
import yaml

config_folder = os.path.expanduser('~') + '/.config/surplus/'
if not os.path.isdir(config_folder): os.makedirs(config_folder)
config_file = config_folder + 'config'


config_default = {}
config_default['Default Folder'] = os.path.expanduser('~')
config_default['Stylesheet'] = config_folder + 'style.qss'
config_default['Places'] = [config_default['Default Folder']]
config_default['Recent'] = []
config_default['Play'] = True
config_default['Show Waveform'] = True

if not os.path.isfile(config_file):
    print('making new config file')
    config = config_default
    with open(config_file, 'w') as config_file_settings:
        yaml.dump(config_default, config_file_settings)
else:
    print('opening existing config')
    with open(config_file, 'rb') as config_file_settings:
        config = yaml.load(config_file_settings)
    #TODO: make sure all the config settings are valid
    if not (type(config) == dict) or \
            not all(setting in config.keys() for setting in config_default.keys()):
        print('bad config, resetting to defaults')
        with open(config_folder + 'config.old', 'w') as config_old:
            yaml.dump(config_old, config)
        config = config_default
        with open(config_file, 'w') as config_file_settings:
            yaml.dump(config_default, config_file_settings)
