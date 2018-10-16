####################################################################################################
#
# DesiTelly Plex Plugin
#
####################################################################################################

import common, common_fnc, updater
import desirulez
import desitvbox
import desitashan
import yodesi

PREFIX = common.PREFIX
NAME = common.NAME
ART = common.ART
ICON = common.ICON

####################################################################################################
def Start():
	ObjectContainer.title1 = NAME
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)
	EpisodeObject.thumb = R(ICON)
	EpisodeObject.art = R(ART)
	VideoClipObject.thumb = R(ICON)
	VideoClipObject.art = R(ART)
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

####################################################################################################

@handler(PREFIX, NAME, art=ART, thumb=ICON)
def MainMenu():
	oc = ObjectContainer()
	if Prefs['show_yodesi']:
		oc.add(DirectoryObject(key=Callback(yodesi.ChannelsMenu, url=yodesi.SITEURL), title=yodesi.SITETITLE, thumb=R(yodesi.SITETHUMB)))
	if Prefs['show_desitvbox']:
		oc.add(DirectoryObject(key=Callback(desitvbox.ChannelsMenu, url=desitvbox.SITEURL), title=desitvbox.SITETITLE, thumb=R(desitvbox.SITETHUMB)))
	if Prefs['show_desitashan']:
		oc.add(DirectoryObject(key=Callback(desitashan.ChannelsMenu, url=desitashan.SITEURL), title=desitashan.SITETITLE, thumb=R(desitashan.SITETHUMB)))
	if Prefs['show_desirulez']:
		oc.add(DirectoryObject(key=Callback(desirulez.TypeMenu, url=desirulez.SITEURL), title=desirulez.SITETITLE, thumb=R(desirulez.SITETHUMB)))
	
	oc.add(DirectoryObject(key = Callback(common_fnc.Pins, title='Pinned Shows'), title = 'Pinned Shows', summary = 'Shows Pinned Shows.', thumb = R(common.ICON_PIN)))
	
	try:
		if updater.update_available()[0]:
			oc.add(DirectoryObject(key = Callback(updater.menu, title='Update Plugin'), title = 'Update (New Available)', thumb = R(common.ICON_UPDATE_NEW)))
		else:
			oc.add(DirectoryObject(key = Callback(updater.menu, title='Update Plugin'), title = 'Update (Running Latest)', thumb = R(common.ICON_UPDATE)))
	except:
		pass

	oc.add(PrefsObject(title = 'Preferences', thumb = R(common.ICON_PREFS)))
	return oc

####################################################################################################