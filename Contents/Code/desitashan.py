import common, common_fnc
import messages
import re

SITETITLE = 'Desi-Tashan'
SITEURL = 'http://www.desi-tashan.ms/'
SITETHUMB = 'icon-desitashan.png'

PREFIX = common.PREFIX
NAME = common.NAME
ART = common.ART
ICON = common.ICON

MC = messages.NewMessageContainer(common.PREFIX, common.TITLE)

####################################################################################################

@route(PREFIX + '/desi-tashan/channels')
def ChannelsMenu(url):
	oc = ObjectContainer(title2=SITETITLE)

	html = HTML.ElementFromURL(url)

	for item in html.xpath("//ul[@id='menu-3']//li//a"):
		try:
			# Channel title
			channel = item.xpath("text()")[0]
	#		Log("Channel = "+channel)
			# Channel link
			link = item.xpath("@href")[0]
			if link.startswith("http") == False:
				link = SITEURL + link
			
			#Log("Channel Link: " + link)
		except:
			channel = item.xpath("./span/text()")
			if(len(channel) != 0):
				channel = channel[0]	
	#			Log("Channel = "+str(channel))
	#			Log("item "+ etree.tostring(item, pretty_print=True))
				# Channel link
				link = item.xpath("@href")[0]
				if link.startswith("http") == False:
					link = SITEURL + link
			else:
				continue

		try:
			image = common.GetThumb(channel.lower())
		except:
			continue

		if channel.lower() in common.GetSupportedChannels():
			oc.add(DirectoryObject(key=Callback(ShowsMenu, url=link, title=channel), title=channel, thumb=image))
		
	# If there are no channels, warn the user
	if len(oc) == 0:
		return ObjectContainer(header=SITETITLE, message=L('ChannelWarning'))

	return oc
	
####################################################################################################

@route(PREFIX + '/desi-tashan/showsmenu')
def ShowsMenu(url, title):
	oc = ObjectContainer(title2=title)
	#Log("Shows Menu: " + url + ":" + title)
	html = HTML.ElementFromURL(url)
	
	for item in html.xpath(".//*[@id='td-outer-wrap']//div//td//li//a"):
		#Log("item "+ etree.tostring(item, pretty_print=True))
		try:
			# Show title
			show = item.xpath("text()")[0]
			#Log("show name: " + show)
			# Show link
			link = item.xpath("@href")[0]
			#Log("show link: " + link)
			if link.startswith("http") == False:
				link = SITEURL + link.lstrip('/')
#				Log("final show link: " + link)	
		except:
			#Log("In Excpetion")
			continue

		# Add the found item to the collection
		oc.add(DirectoryObject(key=Callback(EpisodesMenu, url=link, title=show), title=show))
		
	# If there are no channels, warn the user
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('ShowWarning'))

	return oc

####################################################################################################

@route(PREFIX + '/desi-tashan/episodesmenu')
def EpisodesMenu(url, title):
	oc = ObjectContainer(title2 = unicode(title))

	pageurl = url

	html = HTML.ElementFromURL(pageurl)
	
	for item in html.xpath(".//div[@class='td-block-span6']//h3[@class='entry-title td-module-title']//a"):
		try:
			# Episode title
			episode = unicode(str(item.xpath("text()")[0].strip()))
			
			# episode link
			link = item.xpath("@href")[0]
			if link.startswith("http") == False:
				link = SITEURL + link.lstrip('/')
			Log("Episode: " + episode + " Link: " + link)
		except:
			continue

		# Add the found item to the collection
		if 'Watch'.lower() in episode.lower():
			episode = episode.replace(' Video Watch...','').replace(' Video Watch','')
			oc.add(PopupDirectoryObject(key=Callback(PlayerLinksMenu, url=link, title=episode, type=L('Tv')), title=episode))
	
	# Find the total number of pages
	next_page = ' '
	try:
		next_page = html.xpath("(.//div[@class='page-nav td-pb-padding-side']//a[not (@class='page') and not (@class='last')]//@href)[last()]")
		oc.add(DirectoryObject(key=Callback(EpisodesMenu, url=next_page, title=title), title=L('Pages')))
	except:
		pass
	
	# If there are no channels, warn the user
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('EpisodeWarning'))
		
	if common_fnc.CheckPin(url=url):
		oc.add(DirectoryObject(
			key = Callback(common_fnc.RemovePin, url = url),
			title = "Remove Pin",
			summary = 'Removes the current Show from the Pin list',
			thumb = R(common.ICON_PIN)
		))
	else:
		oc.add(DirectoryObject(
			key = Callback(common_fnc.AddPin, site = SITETITLE, url = url, title = title),
			title = "Pin Show",
			summary = 'Adds the current Show to the Pin list',
			thumb = R(common.ICON_PIN)
		))

	return oc

####################################################################################################

@route(PREFIX + '/desi-tashan/playerlinksmenu')
def PlayerLinksMenu(url, title, type):
	oc = ObjectContainer(title2 = unicode(title))
	
	html = HTML.ElementFromURL(url=url, headers={'Referer': url})
	content = HTML.StringFromElement(html)
	thumb = GetThumb(html)
	
	oc.art = Resource.ContentsOfURLWithFallback(thumb, fallback=R(ART))
	
	if '/images/xfuture.png.pagespeed.ic.WVkcd7CGfW.png' in content:
		return ObjectContainer(header=title, message=L('ComingSoonWarning'))
	
	sources = html.xpath(".//div[@class='td-post-content td-pb-padding-side']//span[contains(text(),'HD')]//text()")
	#if len(sources) == 0:
	#	sources = html.xpath(".//h2[contains(text(),'HD')]//text()")
	for source in sources:
		s_source, i = common_fnc.GetArrayItemMatchInString(common.VALID_SOURCES, source.lower(), False)
		if s_source <> None:
			if '720p' in source.lower():
				if 'single' in source.lower():
					oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source, thumb=thumb), title=(common.VALID_SOURCES[i] + ' HD (Single Link)'), thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
				else:
					oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source, thumb=thumb), title=(common.VALID_SOURCES[i] + ' HD'), thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
			elif 'hd' in source.lower():
				oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source, thumb=thumb), title=(common.VALID_SOURCES[i] + ' HD'), thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
			elif 'dvd' in source.lower():
				oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source, thumb=thumb), title=(common.VALID_SOURCES[i] + ' DVD'), thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
			else:
				oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source, thumb=thumb), title=common.VALID_SOURCES[i], thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
		elif Prefs['allow_unknown_sources']:
			oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source, thumb=thumb), title=source, thumb=R('icon-unknown.png')))
	
# If there are no channels, warn the user
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('PlayerWarning'))
		
	oc.objects.sort(key=lambda obj: obj.title, reverse=False)

	return oc

####################################################################################################

@route(PREFIX + '/desi-tashan/episodelinksmenu')
def EpisodeLinksMenu(url, title, type, thumb):

	oc = ObjectContainer(title2 = unicode(title))
	oc.art = Resource.ContentsOfURLWithFallback(thumb, fallback=R(ART))
	
	html = HTML.ElementFromURL(url)
	# Summary
	summary = GetSummary(html)
	items = GetParts(html, type)

	links = []
	
	OPR = ''

	for item in items:
		
		try:
			# Video site
			videosite = item.xpath(".//text()")[0]
			#Log("Video Site: " + videosite)
			# Video link
			link = item.xpath(".//@href")[0]
			#Log("Link: " + link)
			if link.startswith("http") == False:
				link = link.lstrip('htp:/')
				link = 'http://' + link
			
			# Get video source url and thumb
			link = common_fnc.GetTvURLSource(link,url)
			#Log("Video Site: " + videosite + " Link: " + link + " Thumb: " + thumb)
			
			if 'openload.' in link and Prefs['use_openload_pairing'] and OPR == '':
				if common_fnc.isOpenLoadPairingDone():
					OPR = ' *Paired*'
				else:
					OPR = ' *Pairing Required*'
		except:
			continue

		links.append(link)

		# Add the found item to the collection
		if common_fnc.IsArrayItemInString2(common.VALID_SOURCES_DOMAIN, link, False) or (Prefs['allow_unknown_sources'] and URLService.ServiceIdentifierForURL(link) <> None):
		
			if link.find('openload') != -1 and not common_fnc.is_uss_installed() and Prefs['use_openload_pairing'] == False:
				return MC.message_container('Error', 'UnSupportedServices.bundle Required')
			elif link.find('openload') != -1 and Prefs['use_openload_pairing'] == True:
				link = "desitelly://" + E(JSON.StringFromObject({"title": videosite, "urls": [link], "thumb": thumb, "use_openload_pairing": Prefs['use_openload_pairing']}))
			
			oc.add(VideoClipObject(
				url = link,
				title = '%s%s' % (videosite, OPR),
				thumb = Resource.ContentsOfURLWithFallback(thumb, fallback=R(ICON)),
				art = Resource.ContentsOfURLWithFallback(thumb, fallback=R(ART)),
				summary = summary))
	
	# If there are no channels, warn the user
	if len(oc) == 0 and 'disabled' in links:
		return ObjectContainer(header=title, message=L('DisabledWarning'))
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('SourceWarning'))

	return oc

####################################################################################################

def GetParts(html, keyword):

	xpath_str = ".//div[@class='td-post-content td-pb-padding-side']//span[contains(text(),'"+keyword+"')]//following::p[1]//a"
	
	#Log(xpath_str)
	try:
		items = html.xpath(xpath_str)
	except:
		items = []
	
	return items

####################################################################################################

def GetSummary(html):
	try:
		summary = html.xpath("//h1[@class='entry_title entry-title']/text()")[0]
		#summary = summary.replace(" preview: ","",1)
		#summary = summary.replace("Find out in","",1)
	except:
		summary = ''
	return summary

####################################################################################################

def GetThumb(html):
	try:
		thumb = html.xpath(".//meta[@name='twitter:image']//@content")[0]
		Log ('Thumb: ' + thumb)
	except:
		thumb = R(ICON)
	return thumb
