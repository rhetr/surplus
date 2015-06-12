SurPluS
=======

<b>sur</b>fer/browser for <b>plu</b>gins and <b>s</b>amples

listen to audio samples in an easily-navigable Qt-based file browser made for the task. when you find what you want, drag&drop it into your preferred environment. 

works with carla, drumkv1, ardour and any other app that supports drag-and-drop

plugin browsing (ladspa,dssi,lv2,vst) to come hopefully.
*note: I actually don't know any hosts that currently support dragging-and-dropping plugins (ardour can drag-and-drop plugins across tracks but not from its plugin window), so I don't know when I'll get around to doing this.*

## DEPENDENCIES
python3, numpy, pyqt4, ffmpeg/avconv, sox, yaml

## USAGE
* use arrow keys or jkl; (vi-style) to navigate
* forward slash focuses the input box (escape unfocuses it)
	* typing a forward slash into the input box lets it know that you're going to enter another path
	* otherwise a local, case-insensitive `awk` search is performed in the current directory (I'm not sure how useful this will be but it was fun to figure out how to do)
* view recently used samples (i.e. samples that were dragged out) by selecting *Recent* from the input box dropdown menu
* space/enter triggers playback
* checkbox disables/enables auditioning
* the config file is in $HOME/.config/surplus/config
* add/remove favorite places to the dropdown filepath menu by clicking the +/- button 

## TODO
### usability
* make a proper install script
* config file
    * plugin paths
* more shortcuts
    * tab to switch between plugins/files
    * settings dialog alt+P (just open up a default text editor for the config file)
    * add keybinding for recently used
    * delete recently used with delete key (confirmation dialogue)
    * open current dir in default browser
* sample tagging/smart sample searching
* filePath improvements (probably gonna have to implement a custom widget for this)
    * shortcut to expand dropdown menu
    * tab completion
    * breadcrumbs-style clickable interaction (like nautilus)
* show carla presets

### ui/interaction
* touch interaction

### plugins
* figure out how to get information from plugins

## KNOWN ISSUES
* folders have to be doubleclicked
* if you use the arrow keys down to a file and then click it, it doesn't trigger the first time
* when you follow a symbolic link and go back it takes you to back through the original path
* j is treated differently from left arrow for some reason
* waveforms take a while to load and slow down everything
* peak files are big

## THOUGHTS

it'd be cool if eventually it is extended to utilize keyboard shortcuts to send samples to other LAU programs or something.
