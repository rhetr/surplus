SurPluS
=======

<b>sur</b>fer/browser for <b>plu</b>gins and <b>s</b>amples

listen to audio samples in an easily-navigable Qt-based file browser made for the task. when you find what you want drag&drop it into your preferred environment to work with this so far). It'd be cool if eventually it is extended to utilize keyboard shortcuts to send samples to other LAU programs or something.

currently works with carla and drumkv1.

plugin browsing (ladspa,dssi,lv2,vst) to come hopefully.

DEPENDENCIES
------------
numpy, pyqt4, ffmpeg/avconv, sox, yaml

USAGE
-----
* checkbox to disable/enable playback
* config file in $HOME/.config/surplus/config


KEYBOARD SHORTCUTS
------------------
* use arrow keys or jkl; (vim-style) to navigate
* forward slash focuses the path (escape unfocuses it)
* space/enter triggers playback

TODO
----
###usability
* make a proper install script
* make favorites (favoriting directories as well as files and plugins)
* config file
    * plugin paths
* more shortcuts
    * tab to switch between plugins/files
    * settings dialog ctrl+P
    * make shortcut for recently used
* sample tagging/smart sample searching

###ui/interaction
* move scrollbar to left side underneath tabs
* touch interaction

###plugins
* figure out how to get information from plugins

KNOWN ISSUES
------------
* folders have to be doubleclicked
* if you use the arrow keys down to a file and then click it, it doesn't trigger the first time
* when you follow a symbolic link and go back it takes you to back through the original path
* j is treated differently from left arrow for some reason
* waveforms take a while to load and slow down everything
* peak files are big
