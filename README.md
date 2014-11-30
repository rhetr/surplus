SurPluS
=======

<b>sur</b>fer/browser for <b>plu</b>gins and <b>s</b>amples

listen to audio samples in an easily-navigable Qt-based file browser made for the task. when you find what you want drag&drop it into your preferred environment (theoretically--in practice I've only found [Carla](http://github.com/falkTX/Carla) to work with this so far). It'd be cool if eventually it is extended to utilize keyboard shortcuts to send samples to other LAU programs or something.

plugin browsing (ladspa,dssi,lv2,vst) to come hopefully.


USAGE
-----
TODO


SHORTCUTS
---------
* arrow keys navigate in/out of directories
* space + enter trigger playback

TODO
----
###sample interaction
* checkbox to disable/enable playback
* show waveform
* scrolling through long samples

###usability
* make favorites (favoriting directories as well as files and plugins)
* settings dialogue
    * default location
    * plugin paths
* more shortcuts
    * tab to switch between plugins/files
    * slash to search
    * settings dialog ctrl+P
* sample tagging/smart sample searching

###ui/interaction
* remove outline from selection box
* selection box resizes with window
* move scrollbar to left side underneath tabs
* touch interaction

###plugins
* figure out how to get information from plugins

###programming structure
* use either camelCase or snake_case not both
* use qt signals instead of setting fields
* don't use play

KNOWN BUGS
----------
* select box behavior resets if you unfocus&refocus window
