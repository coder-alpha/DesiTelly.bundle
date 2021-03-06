################################################################################
TITLE = L('Title')
VERSION = '0.13' # Release notation (x.y - where x is major and y is minor)
GITHUB_REPOSITORY = 'coder-alpha/DesiTelly.bundle'
PREFIX = "/video/desitelly"
################################################################################

NAME     = L('Title')
ART      = 'art-default.jpg'
ICON     = 'icon-default.png'
ICON_PIN = "icon-pin.png"
ICON_PREFS = "icon-prefs.png"
ICON_UPDATE = "icon-update.png"
ICON_UPDATE_NEW = "icon-update-new.png"

STARPLUS = 'Star Plus'
ZEETV = 'Zee Tv'
SONYTV = 'Sony Tv'
LIFEOK = 'Life OK'
SAHARAONE = 'Sahara One'
STARJALSHA = 'Star Jalsha'
COLORS = 'Colors Channel'
SABTV = 'Sab TV'
STARPRAVAH = 'Star Pravah'
MTV = 'MTV (India/Pakistan)'
CHANNELV = 'Channel [V]'
BINDASSTV = 'Bindass TV'
UTVSTARS = 'UTV Stars'
NEWS = 'News Channels'
STARONE = 'Star One'
XINXMEDIA = '9X INX Media'
NDTV = 'NDTV Imagine'
COLORSTV = 'Colors'
MTVIN = 'MTV India'
CHANNELVV = 'Channel V'
BINDASS = 'Bindass'
COLORSTVCHAN = 'Colors Tv Channel'
COLORS_TV = 'Colors Tv'
SABTVCHAN = 'SabTv Channel'
SONYPAL = 'Sony Pal'
DDNATIONAL = 'DD National'
ZINDAGITV = 'Zindagi Tv'
BIGMAGIC = 'Big Magic'
BIGTHRILL = 'Big Thrill'
RISHTEYTV = 'Rishtey Tv'
ZEEANMOL = 'Zee Anmol'
STARUTSAV = 'Star Utsav'
MASTI = 'Masti'
ZINGTV = 'Zing Tv'
ZOOMTV = 'Zoom Tv'
ABPNEWS = 'ABP News'
AAJTAKNEWS = 'Aaj Tak News Channel'
ZEENEWS = 'Zee News Channel'
IBN7 = 'IBN7'
NDTVINDIA = 'NDTV India'
E24 = 'E24/News 24'
UTVSTARSNEWS = 'UtV Stars (News)'
NEWSEXPRESS = 'News Express'
SAHARASAMAY = 'Sahara Samay'
ZEEMARATHI = 'Zee Marathi'
ETVBANGLA = 'ETv Bangla'
ETVMARATHI = 'ETV Marathi'
ZEEBANGLA = 'Zee Bangla'
STARVIJAY = 'Star Vijay'
MAHUAATV = 'Mahuaa Tv'
PTCPUNJABI = 'PTC Punjabi'
STARWORLDHD = 'Star World Premiere HD'
STARWORLD = 'Star World'
STARBHARAT = 'Star Bharat'
ZEECAFE = 'Zee Cafe'
PAKCHAN = 'Pak Channels'
ZEENEXT = 'Zee-Next'
REALTV = 'Real Tv'
FIRANGI = 'FIRANGI'
ZEEMUZIC = 'Zee Muzic'

# Added by Coder-Alpha
ANDTV = '& Tv'
EPIC = 'EPIC'

# Yo-Desi
COLORSMARATHI = 'Colors Marathi'
COLORSBANGLA = 'Colors Bangla'
ZEEYUVA = 'Zee Yuva'

# DesiBoxTv
ANDTV2 = 'And TV'
SONYPAL2 = 'Pal'
MTVIN2 = 'MTV'
ZINDAGITV2 = 'Zindagi'

#DesiTashan
TV_NEWS = 'TV News'

VALID_SOURCES_DOMAIN = ['dailymotion.','playwire.','vidshare.','openload.','playu.', 'cloudy.', 'vmg.','watchvideo','tvlogy','google','mediatv.','vidwatch','speedwatch.us','tune.pk','vidoza.','dailytv.','thevideobee','videobee','irshare','vkprime']

VALID_SOURCES = ['Dailymotion','Flash Player','Flash','Playwire','Letwatch','Openload','PlayU','StreamHD','HDStream','Watchvideo','TvLogy','Google','VidWatch','Vid Watch','Vidwatch','SpeedWatch','Speedwatch','Speed','TunePK','Tunepk','Tune','ViDoza','DailyTV','TheVideoBee','Videobee','VK Prime']

VALID_SOURCES_ICONS = ['dailymotion','flashplayer','flashplayer','flashplayer','letwatchus','openload','playu','vmg','vmg','source-watchvideo','tvlogy','google','vidwatch','vidwatch','vidwatch','speedwatch','speedwatch','speedwatch','tunepk','tunepk','tunepk','vidoza','dailytv','thevideobee','videobee','vkprime']

DISABLED_SOURCES = ['domain-defined']

####################################################################################################

def GetSupportedChannels():
	return [
		STARPLUS.lower(),
		STARBHARAT.lower(),
		ZEETV.lower(), 
		SONYTV.lower(), 
		LIFEOK.lower(), 
		SAHARAONE.lower(), 
		STARJALSHA.lower(), 
		COLORS.lower(), 
		SABTV.lower(), 
		STARPRAVAH.lower(), 
		MTV.lower(), 
		CHANNELV.lower(), 
		BINDASSTV.lower(), 
		UTVSTARS.lower(),
		STARONE.lower(),
		XINXMEDIA.lower(),
		NDTV.lower(),
		COLORSTV.lower(),
		COLORS_TV.lower(),
		MTVIN.lower(),
		CHANNELVV.lower(),
		BINDASS.lower(),
		COLORSTVCHAN.lower(),
		SABTVCHAN.lower(),
		SONYPAL.lower(),
		DDNATIONAL.lower(),
		ZINDAGITV.lower(),
		BIGMAGIC.lower(),
		BIGTHRILL.lower(),
		RISHTEYTV.lower(),
		ZEEANMOL.lower(),
		STARUTSAV.lower(),
		MASTI.lower(),
		ZINGTV.lower(),
		ZOOMTV.lower(),
		ABPNEWS.lower(),
		AAJTAKNEWS.lower(),
		ZEENEWS.lower(),
		IBN7.lower(),
		NDTVINDIA.lower(),
		E24.lower(),
		UTVSTARSNEWS.lower(),
		NEWSEXPRESS.lower(),
		SAHARASAMAY.lower(),
		ZEEMARATHI.lower(),
		ETVBANGLA.lower(),
		ETVMARATHI.lower(),
		ZEEBANGLA.lower(),
		STARVIJAY.lower(),
		MAHUAATV.lower(),
		PTCPUNJABI.lower(),
		STARWORLD.lower(),
		ZEECAFE.lower(),
		PAKCHAN.lower(),
		ZEENEXT.lower(),
		REALTV.lower(),
		FIRANGI.lower(),
		ZEEMUZIC.lower(),
		ANDTV.lower(),
		ANDTV2.lower(),
		SONYPAL2.lower(),
		MTVIN2.lower(),
		ZINDAGITV2.lower(),
		EPIC.lower(),
		COLORSMARATHI.lower(),
		COLORSBANGLA.lower(),
		ZEEYUVA.lower(),
		ZEEMARATHI.lower(),
		ZEEBANGLA.lower(),
		TV_NEWS.lower()
	]

####################################################################################################
	
def GetThumb(channel):
	icon = R('icon-no-thumb.png')

	if channel == STARPLUS.lower():
		icon = R('icon-starplus.png')
	elif channel == ZEETV.lower():
		icon = R('icon-zeetv.png')
	elif channel == SONYTV.lower():
		icon = R('icon-sonytv.png')
	elif channel == LIFEOK.lower():
		icon = R('icon-lifeok.png')
	elif channel == SAHARAONE.lower():
		icon = R('icon-saharaone.png')
	elif channel == STARJALSHA.lower():
		icon = R('icon-starjalsha.png')
	elif channel == COLORS.lower() or channel == COLORSTV.lower() or channel == COLORSTVCHAN.lower() or channel == COLORS_TV.lower():
		icon = R('icon-colors.png')
	elif channel == SABTV.lower() or channel == SABTVCHAN.lower():
		icon = R('icon-sabtv.png')
	elif channel == STARPRAVAH.lower():
		icon = R('icon-starpravah.png')
	elif channel == MTV.lower() or channel == MTVIN.lower() or channel == MTVIN2.lower():
		icon = R('icon-mtv.png')
	elif channel == CHANNELV.lower() or channel == CHANNELVV.lower():
		icon = R('icon-channelv.png')
	elif channel == BINDASSTV.lower() or channel == BINDASS.lower():
		icon = R('icon-bindasstv.png')
	elif channel == UTVSTARS.lower() or channel == UTVSTARSNEWS.lower():
		icon = R('icon-utvstars.png')
	elif channel == NEWS.lower():
		icon = R('icon-indianews.png')
	elif channel == STARONE.lower():
		icon = R('icon-starone.png')
	elif channel == XINXMEDIA.lower():
		icon = R('icon-9xinxmedia.png')
	elif channel == NDTV.lower():
		icon = R('icon-ndtv.png')
	elif channel == SONYPAL.lower() or channel == SONYPAL2.lower():
		icon = R('icon-sonypal.png')
	elif channel == DDNATIONAL.lower():
		icon = R('icon-ddnational.png')
	elif channel == ZINDAGITV.lower() or channel == ZINDAGITV2.lower():
		icon = R('icon-zindagitv.png')
	elif channel == BIGMAGIC.lower():
		icon = R('icon-bigmagic.png')
	elif channel == BIGTHRILL.lower():
		icon = R('icon-bigthrill.png')
	elif channel == RISHTEYTV.lower():
		icon = R('icon-rishteytv.png')
	elif channel == ZEEANMOL.lower():
		icon = R('icon-zeeanmol.png')
	elif channel == STARUTSAV.lower():
		icon = R('icon-starutsav.png')
	elif channel == MASTI.lower():
		icon = R('icon-masti.png')
	elif channel == ZINGTV.lower():
		icon = R('icon-zingtv.png')
	elif channel == ZOOMTV.lower():
		icon = R('icon-zoomtv.png')
	elif channel == ABPNEWS.lower():
		icon = R('icon-abpnews.png')
	elif channel == AAJTAKNEWS.lower():
		icon = R('icon-aajtaknews.png')
	elif channel == ZEENEWS.lower():
		icon = R('icon-zeenews.png')
	elif channel == IBN7.lower():
		icon = R('icon-ibn7.png')
	elif channel == NDTVINDIA.lower():
		icon = R('icon-ndtvindia.png')
	elif channel == E24.lower():
		icon = R('icon-e24.png')
	elif channel == NEWSEXPRESS.lower():
		icon = R('icon-newsexpress.png')
	elif channel == SAHARASAMAY.lower():
		icon = R('icon-saharasamay.png')
	elif channel == ZEEMARATHI.lower():
		icon = R('icon-zeemarathi.png')
	elif channel == ETVBANGLA.lower():
		icon = R('icon-etvbangla.png')
	elif channel == ETVMARATHI.lower():
		icon = R('icon-etvmarathi.png')
	elif channel == ZEEBANGLA.lower():
		icon = R('icon-zeebangla.png')
	elif channel == STARVIJAY.lower():
		icon = R('icon-starvijay.png')
	elif channel == MAHUAATV.lower():
		icon = R('icon-mahuaatv.png')
	elif channel == PTCPUNJABI.lower():
		icon = R('icon-ptcpunjabi.png')
	elif channel == STARWORLDHD.lower():
		icon = R('icon-starworldpremierehd.png')
	elif channel == STARWORLD.lower():
		icon = R('icon-starworld.png')
	elif channel == ZEECAFE.lower():
		icon = R('icon-zeecafe.png')
	elif channel == PAKCHAN.lower():
		icon = R('icon-pakchannels.png')
	elif channel == ZEENEXT.lower():
		icon = R('icon-zeenext.png')
	elif channel == REALTV.lower():
		icon = R('icon-realtv.png')
	elif channel == FIRANGI.lower():
		icon = R('icon-firangi.png')
	elif channel == ZEEMUZIC.lower():
		icon = R('icon-zeemuzic.png')
	elif channel == ANDTV.lower() or channel == ANDTV2.lower():
		icon = R('icon-&TV.png')
	elif channel == EPIC.lower():
		icon = R('icon-epic.png')
	elif channel == STARBHARAT.lower():
		icon = R('icon-starbharat.png')

	return icon

# author: Twoure
# source: https://github.com/Twoure/HindiMoviesOnline.bundle/blob/master/Contents/Code/messages.py
#
class NewMessageContainer(object):
	def __init__(self, prefix, title):
		self.title = title
		Route.Connect(prefix + '/message', self.message_container)

	def message_container(self, header, message):
		"""Setup MessageContainer depending on Platform"""

		if Client.Platform in ['Plex Home Theater', 'OpenPHT']:
			oc = ObjectContainer(
				title1=self.title, title2=header, no_cache=True,
				no_history=True, replace_parent=True
				)
			oc.add(PopupDirectoryObject(title=header, summary=message))
			return oc
		else:
			return MessageContainer(header, message)