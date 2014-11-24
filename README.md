Samplefucker
============

listen to audio samples in an easily-navigable Qt-based file browser made for the task. when you find what you want drag&drop it into your preferred environment (theoretically--in practice I've only found [Carla](http://github.com/falkTX/Carla) to work with this so far). It'd be cool if eventually it is extended to utilize keyboard shortcuts to send samples to other LAU programs or something.

plugin browsing (ladspa,dssi,lv2,vst) to come hopefully.

SHORTCUTS
---------
* arrow keys navigate in/out of directories
* space + enter trigger playback

TODO
----
* shortcuts
    * tab to switch between plugins/files
    * slash to search
    * settings dialog ctrl+P
* use qt signals instead of setting fields
* checkbox to disable/enable playback
* show waveform
* settings dialogue
    * default location
    * plugin paths
* make favorites
* selection box resizes with window
* remove outline from selection box
* figure out how to get information from plugins
* don't use play?

KNOWN BUGS
----------
* select box behavior resets if you unfocus&refocus window

possible features
-----------------
* smart sample searching (probably not)
* touch interaction (probably)
