SurPluS
=======

<b>sur</b>fer/browser for <b>plu</b>gins and <b>s</b>amples

listen to audio samples in an easily-navigable Qt-based file browser made for the task. when you find what you want drag&drop it into your preferred environment to work with this so far). It'd be cool if eventually it is extended to utilize keyboard shortcuts to send samples to other LAU programs or something.

currently works with carla and drumkv1.

plugin browsing (ladspa,dssi,lv2,vst) to come hopefully.

DEPENDENCIES
------------
numpy, pyqt4, ffmpeg/avconv, sox

USAGE
-----
TODO


KEYBOARD SHORTCUTS
------------------
* left/right arrow keys navigate in/out of directories
* up/down/home/end arrow keys navigate inside a directory
* forward slash focuses the path (escape unfocuses it)
* space/enter trigger playback

TODO
----
###sample interaction
* checkbox to disable/enable playback
* show waveform
* scrolling through long samples

###usability
* make favorites (favoriting directories as well as files and plugins)
* make "recently used"
* settings dialogue
    * default location
    * plugin paths
* more shortcuts
    * tab to switch between plugins/files (implemented but plugin browsing isn't)
    * settings dialog ctrl+P
* sample tagging/smart sample searching

###ui/interaction
* selection box resizes with window
* move scrollbar to left side underneath tabs
* touch interaction

###plugins
* figure out how to get information from plugins

###programming structure
* use QListView instead of QGraphicsView 

KNOWN ISSUES
------------
* select box behavior resets if you unfocus&refocus window
* waveforms take a while to load and slow down everything
* peak files are big
