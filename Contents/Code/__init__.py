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

####################################################################################################

@handler(PREFIX, NAME, art=ART, thumb=ICON)
def MainMenu():
	oc = ObjectContainer()
	oc.add(DirectoryObject(key=Callback(yodesi.ChannelsMenu, url=yodesi.SITEURL), title=yodesi.SITETITLE, thumb=R(yodesi.SITETHUMB)))
	oc.add(DirectoryObject(key=Callback(desitvbox.ChannelsMenu, url=desitvbox.SITEURL), title=desitvbox.SITETITLE, thumb=R(desitvbox.SITETHUMB)))
	oc.add(DirectoryObject(key=Callback(desitashan.ChannelsMenu, url=desitashan.SITEURL), title=desitashan.SITETITLE, thumb=R(desitashan.SITETHUMB)))
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