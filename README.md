DesiTelly.bundle
===================
Plex Media Server plug-in designed for Desi Entertainment
[Plex Support thread] (TBA)
[Plex Support thread (old)] (https://forums.plex.tv/discussion/107492/req-indian-tv-shows/p1)

System Requirements
===================
- **Plex Media Server:**
	- Tested Working:
		- Windows
		- Linux (Ubuntu) (Updater to work - cd to Plex Plugin's dir & use 'sudo chown -R plex:plex DesiTelly.bundle')
- **Plex Clients:**
	- Tested Working:
		- Plex Home Theater
		- Plex/Web
		- Samsung Plex App
		- Android Kit-Kat (Samsung Galaxy S3)
		- iOS (Apple iPhone6)

How To Install
==============
- Download the latest version of the plugin.
- Unzip and rename folder to "DesiTelly.bundle"
- Delete any previous versions of this bundle
- Copy DesiTelly.bundle into the PMS plugins directory under your user account:
	- Windows 7, Vista, or Server 2008: 
		C:\Users[Your Username]\AppData\Local\Plex Media Server\Plug-ins
	- Windows XP, Server 2003, or Home Server: 
		C:\Documents and Settings[Your Username]\Local Settings\Application Data\Plex Media Server\Plug-ins
	- Mac/Linux: 
        ~/Library/Application Support/Plex Media Server/Plug-ins
- Restart PMS

Important Notes
==============
- Currently only Dailymotion, Flash/Playwire, PlayU, Letwatch/Vidshare & VMG host is supported well.
- More hosts can be enabled using USS (read below under Preferences/Options setting). [UnSupportedServices.bundle](https://github.com/Twoure/UnSupportedServices.bundle) must be installed and updated to dev branch to use Openload host when available for video links
- Movie support for DesiRulez is included but YMMV (installing USS is highly recommended)
- This plugin builds from my older version located [here] (https://github.com/coder-alpha/DesiTV.bundle)

Preferences/Options setting
==============
- Allow Hosts natively NOT supported by this plugin: This options when enabled will list all host sources available, however, based on URLServices installed on your Plex server the capability to play a video will be determined. If you plan to enable this feature installing USS above is highly recommended.
- Consolidate Parts - Flash/Playwire [Desitvbox]: This feature groups split-parts of a single show as one playable item. Currently only enabled for Flash/Playwire source under DesiTvBox. This might be expanded to others based on feedback.

Known Issues
==============
- The page schema and naming convention is very inconsistent so even though the parser has many fallbacks it may still fail to retrieve the links. If you find such cases please post details of such shows.
- Incorrectly marked videos will not play.

Acknowledgements
==============

- Credits to [b-slick] (https://forums.plex.tv/index.php/topic/107492-req-indian-tv-shows/): for developing the original code
- Credits to [mohit310] (https://github.com/mohit310/DesiTV.bundle) and [hussamnasir] (https://github.com/hussamnasir/DesiTV.bundle) for contributions. Check out their forks as well.
- Thanks to [Twoure] (https://github.com/Twoure/) for developing the UnSupportedServices.bundle and help with split-part playback
