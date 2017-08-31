import common, common_fnc
import urlparse
import re
import time
import datetime
import messages

SITETITLE = L('DesiRulezTitle')
SITEURL = 'http://www.desirulez.me/'
SITETHUMB = 'icon-desirulez.png'
BOLLYWOODMOVIES = 'http://www.desirulez.net/forums/260-Bollywood-Movies?s=ff8112e19bee5e07f0e95696812ae217'

DESIRULEZMOVIES = ['Latest & Exclusive Movie HQ']

PREFIX = common.PREFIX
NAME = common.NAME
ART = common.ART
ICON = common.ICON

MC = messages.NewMessageContainer(common.PREFIX, common.TITLE)

####################################################################################################

@route(PREFIX + '/desirulez/typemenu')
def TypeMenu(url):
	oc = ObjectContainer(title2=SITETITLE)
	
	# Add the item to the collection
	oc.add(DirectoryObject(key=Callback(ChannelsMenu, url=url), title=L('Tv'), thumb=R('icon-default.png')))
	oc.add(DirectoryObject(key=Callback(MovieTypeMenu, url=url), title=L('Movies'), thumb=R('icon-default.png')))
	
	# If there are no channels, warn the user
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('TypeWarning'))

	return oc

####################################################################################################

@route(PREFIX + '/desirulez/movietype')
def MovieTypeMenu(url):
	oc = ObjectContainer(title2=SITETITLE)

	html = HTML.ElementFromURL(url)

	for item in html.xpath("//li[@id='cat17']//h2[@class='forumtitle']/a"):
		try:
			# Movie Section
			section = item.xpath("./text()")[0]

			# Section Link
			link = item.xpath("./@href")[0]
			if link.startswith("http") == False:
				link = SITEURL + link
		except:
			continue

		if section in DESIRULEZMOVIES:
			oc.add(DirectoryObject(key=Callback(MovieListMenu, url=link, title=section), title=section))
			
	oc.add(DirectoryObject(key=Callback(MovieSectionMenu, url=BOLLYWOODMOVIES, title=L('BollywoodMovies')), title=L('BollywoodMovies')))
		
	# If there are no channels, warn the user
	if len(oc) == 0:
		return ObjectContainer(header=SITETITLE, message=L('MovieWarning'))

	return oc

####################################################################################################
@route(PREFIX + '/desirulez/movielist')
def MovieListMenu(url, title, page=1, pages=1):
	oc = ObjectContainer(title2=title)

	pageurl = url + '/page' + str(page)
	
	html = HTML.ElementFromURL(pageurl)
	
	for item in html.xpath("//div[@class='inner']/h3[@class='threadtitle']/a[contains(@id,'thread_title') and contains(text(),'Watch')]"):
		try:
			# Movie title
			movie = item.xpath("./text()")[0]
			
			# Movie link
			link = item.xpath("./@href")[0]
			if link.startswith("http") == False:
				link = SITEURL + link
		except:
			continue

		# Add the found item to the collection
		oc.add(PopupDirectoryObject(key=Callback(PlayerLinksMenu, url=link, title=movie, type=L('Movies')), title=movie))
	
	# Find the total number of pages
	if pages == 1:
		for items in html.xpath("//span/a[contains(text(),'Page') and @class='popupctrl']"):
			try:
				pages = int((items.xpath("./text()")[0].split()[-1]).strip())
			except:
				continue

	# Add the next page link if exists
	if page < pages:
		oc.add(DirectoryObject(key=Callback(MovieListMenu, url=url, title=title, page=int(page)+1, pages=pages), title=L('Pages')))
	
	# If there are no channels, warn the user
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('EpisodeWarning'))

	return oc

####################################################################################################

@route(PREFIX + '/desirulez/moviesection')
def MovieSectionMenu(url, title):
	oc = ObjectContainer(title2=SITETITLE)
	
	html = HTML.ElementFromURL(url)
	
	for item in html.xpath("//div[@class='forumbitBody']//h2[@class='forumtitle']/a"):
		try:
			# Movie Section
			section = item.xpath("./text()")[0]
	
			# Section Link
			link = item.xpath("./@href")[0]
			if link.startswith("http") == False:
				link = SITEURL + link
		except:
			continue
	
		if section != 'Upcoming Movie Trailers':
			oc.add(DirectoryObject(key=Callback(MovieListMenu, url=link, title=section), title=section))
		
	# If there are no channels, warn the user
	if len(oc) == 0:
		return ObjectContainer(header=SITETITLE, message=L('MovieWarning'))
	
	return oc

####################################################################################################

@route(PREFIX + '/desirulez/channels')
def ChannelsMenu(url):
	oc = ObjectContainer(title2=SITETITLE)

	html = HTML.ElementFromURL(url)

	for item in html.xpath("//li[@id='cat41']//div[@class='foruminfo td']"):
		try:
			# Channel title
			channel = item.xpath("./div/div/div/h2/a/text()")[0]

			# Channel link
			link = item.xpath("./div/div/div/h2/a/@href")[0]
			if link.startswith("http") == False:
				link = SITEURL + link
		except:
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

@route(PREFIX + '/desirulez/showsmenu')
def ShowsMenu(url, title):
	oc = ObjectContainer(title2=title)

	html = HTML.ElementFromURL(url)
	
	for item in html.xpath("//div[@class='forumbitBody']//div[@class='foruminfo']"):
		try:
			# Show title
			show = item.xpath("./div/div/div/h2/a/text()")[0]
			
			# Show link
			link = item.xpath("./div/div/div/h2/a/@href")[0]
			if link.startswith("http") == False:
				link = SITEURL + link
		except:
			continue

		# Add the found item to the collection
		oc.add(DirectoryObject(key=Callback(EpisodesMenu, url=link, title=show), title=show))
		
	# If there are no channels, warn the user
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('ShowWarning'))

	return oc

####################################################################################################

@route(PREFIX + '/desirulez/episodesmenu')
def EpisodesMenu(url, title, page=1, pages=1):
	oc = ObjectContainer(title2=title)

	pageurl = url + '/page' + str(page)
	
	html = HTML.ElementFromURL(pageurl)
	
	for item in html.xpath("//h3[@class='threadtitle']/a[contains(text(),'Watch Online')]"):
		try:
			# Episode title
			episode = item.xpath("./text()")[0]
			
			# episode link
			link = item.xpath("./@href")[0]
			if link.startswith("http") == False:
				link = SITEURL + link
		except:
			continue

		# Add the found item to the collection
		oc.add(PopupDirectoryObject(key=Callback(PlayerLinksMenu, url=link, title=episode, type=L('Tv')), title=episode))
	
	# Find the total number of pages
	if pages == 1:
		for items in html.xpath("//span/a[contains(text(),'Page') and @class='popupctrl']"):
			try:
				pages = int((items.xpath("./text()")[0].split()[-1]).strip())
			except:
				continue
			
	# Add the next page link if exists
	if page < pages:
		oc.add(DirectoryObject(key=Callback(EpisodesMenu, url=url, title=title, page=int(page)+1, pages=pages), title=L('Pages')))
	
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

@route(PREFIX + '/desirulez/playerlinksmenu')
def PlayerLinksMenu(url, title, type):
	oc = ObjectContainer(title2=title)
	
	html = HTML.ElementFromURL(url=url, headers={'Referer': url})
	content = HTML.StringFromElement(html)
	
	sources = html.xpath(".//div[@class='content hasad']//b//font[@color='Red']/text()")
	
	# Add the item to the collection
	if type == "TV":
		if len(sources) == 0 and Prefs['allow_unknown_sources']:
			sources = html.xpath(".//div[@class='content hasad']//font[@color='Red']/text()")
		elif len(sources) == 0 and not Prefs['allow_unknown_sources']:
			return ObjectContainer(header=title, message=L('EnableHostOption'))
		for source in sources:
			s_source, i = common_fnc.GetArrayItemMatchInString(common.VALID_SOURCES, source, True)
			Log(s_source)
			if s_source == None:
				s_source, i = common_fnc.GetArrayItemMatchInString(common.VALID_SOURCES, source.lower(), False)
				Log(s_source)
			if s_source <> None:
				if '720p' in source.lower():
					if 'single' in source.lower():
						oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=common.VALID_SOURCES[i], quality='720p HD Quality Single Link'), title=(common.VALID_SOURCES[i] + ' HD (Single Link)'), thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
					else:
						oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=common.VALID_SOURCES[i], quality='720p'), title=(common.VALID_SOURCES[i] + ' HD'), thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
				elif 'dvd' in source.lower():
					oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=common.VALID_SOURCES[i], quality='DVD'), title=(common.VALID_SOURCES[i] + ' DVD'), thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
				else:
					oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=common.VALID_SOURCES[i], quality='SD'), title=common.VALID_SOURCES[i], thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
			elif Prefs['allow_unknown_sources'] and 'download' not in source.lower():
				suffix = ''
				if 'single' in source.lower():
					quality='720p HD Quality Single Link'
					source = source.replace(quality, '').strip()
					suffix = ' HD (Single Link)'
				elif '720p' in source.lower():
					quality = '720p'
					suffix = ' HD'
				elif 'dvd' in source.lower():
					quality = 'DVD'
					suffix = ' DVD'
				elif 'sd' in source.lower():
					quality = 'SD'
					suffix = ' SD'
				else:
					quality = ''
					suffix = ''
				source = source.replace('720p HD Quality Online Links', '').strip()
				key = source.split(' ')
				if len(key) > 0:
					key = key[0]
				oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source, quality=quality, key=key), title=source + suffix, thumb=R('icon-unknown.png')))
	elif type == "Movies":
		if len(sources) > 0:
			all_sources = []
			for source in sources:
				s_source, i = common_fnc.GetArrayItemMatchInString(common.VALID_SOURCES, source.lower(), False)
				
				f_source = common.VALID_SOURCES[i]
				if (f_source) in all_sources:
					f_source = f_source + ' - Split Parts'
				all_sources.append(f_source)
				if s_source <> None:
					oc.add(DirectoryObject(key=Callback(MovieLinksMenu, url=url, title=title, type=common.VALID_SOURCES[i]), title=f_source, thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
				elif Prefs['allow_unknown_sources'] and 'download' not in source.lower():
					source = source.replace('Watch Online - ','')
					key = source.split(' ')
					if len(key) > 0:
						key = key[0]
					oc.add(DirectoryObject(key=Callback(MovieLinksMenu, url=url, title=title, type=source, key=key), title=source, thumb=R('icon-unknown.png')))
			if len(oc) == 0 and not Prefs['allow_unknown_sources']:
				return ObjectContainer(header=title, message=L('EnableHostOption'))
		else:
			if Prefs['allow_unknown_sources']:
				# Get thumb
				try:
					thumb = html.xpath(".//div[@class='content hasad']//@src")[0]
				except:
					thumb = ''
				if len(sources) == 0:
					sources = html.xpath(".//blockquote/div/div[2]/pre/text()")
					if len(sources) > 0:
						sources = sources[0].replace('\n', ' ')
						sources = sources.split(' or ')
				if len(sources) == 0:
					sources = html.xpath(".//div[@class='content hasad']//a[@target='_blank']//@href")
				if len(sources) > 0:
					for source in sources:
						link = source.strip()
						p = re.compile(ur'^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$')
						host = re.search(p, link).group(3)
						if URLService.ServiceIdentifierForURL(link) <> None:
							oc.add(DirectoryObject(key=Callback(IntermediateMovieLinksMenu, url=link, title=title, hostlink=host, thumb=thumb), title=host, thumb=Resource.ContentsOfURLWithFallback(thumb, fallback=R(ICON))))
			else:
				return ObjectContainer(header=title, message=L('EnableHostOption'))
		
	# If there are no channels, warn the user
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('PlayerWarning'))

	return oc

####################################################################################################

@route(PREFIX + '/desirulez/intermediatemovielinksmenu')
def IntermediateMovieLinksMenu(url, title, hostlink, thumb):
	oc = ObjectContainer(title2=title)
	
	vidsRemoved = common_fnc.CheckURLSource(url=url, referer=url, key=hostlink, string=url, stringMatch=True)
	if 'disabled' not in vidsRemoved:
		oc.add(VideoClipObject(
			url = url, 
			title = hostlink,
			art = Resource.ContentsOfURLWithFallback(thumb, fallback=R(ART)),
			thumb = Resource.ContentsOfURLWithFallback(thumb, fallback=R(ICON))))
	
	if len(oc) == 0 and 'disabled' in vidsRemoved:
		return ObjectContainer(header=title, message=L('DisabledWarning'))
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('SourceWarning'))
	
	return oc
	
####################################################################################################

@route(PREFIX + '/desirulez/movielinksmenu')
def MovieLinksMenu(url, title, type, key=None):
	
	oc = ObjectContainer(title2=title)
	html = HTML.ElementFromURL(url)
	# Get thumb
	try:
		thumb = html.xpath(".//div[@class='content hasad']//@src")[0]
	except:
		thumb = ''
			
	#Log("thumb: "+thumb)
	
	if 'Split Parts' in type:
		isSplitParts=True
	else:
		isSplitParts=False
	if "Openload" in type:
		if not common_fnc.is_uss_installed():
			return MC.message_container('Error', 'UnSupportedServices.bundle Required')
		items = GetMovieSources(html, type, isSplitParts)
	elif "Openload" not in type:
		items = GetMovieSources(html, type, isSplitParts)
	else:
		items = []
		
	if len(items) == 0:
		return ObjectContainer(header=title, message=L('SourceWarning'))
		
	links = []

	for item in items:
		try:
			# Video site
			videosite = item.xpath("./text()")[0]
			# Video link
			link = item.xpath("./@href")[0]
			if link.startswith("http") == False:
				link = link.lstrip('htp:/')
				link = 'http://' + link
			# Show date
			#date = GetMoviePostDate(html)
			# Get video source url
			link = common_fnc.GetTvURLSource(link,url,date='',key=key)
			Log("Video Site: " + videosite + " Link: " + link + " Thumb: " + thumb)
		except:
			continue
		
		links.append(link)
		
		# Add the found item to the collection
		if common_fnc.IsArrayItemInString2(common.VALID_SOURCES_DOMAIN, link, False) or (Prefs['allow_unknown_sources'] and URLService.ServiceIdentifierForURL(link) <> None):
			oc.add(VideoClipObject(
				url = link, 
				title = videosite, 
				thumb = Resource.ContentsOfURLWithFallback(thumb, fallback=R(ICON))))

	# If there are no channels, warn the user
	if len(oc) == 0 and 'disabled' in links:
		return ObjectContainer(header=title, message=L('DisabledWarning'))
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('SourceWarning'))

	return oc
	
####################################################################################################
@route(PREFIX + '/desirulez/episodelinksmenu')
def EpisodeLinksMenu(url, title, type, quality, key=None):
	
	oc = ObjectContainer(title2=title)

	html = HTML.ElementFromURL(url=url, headers={'Referer': url})
	content = HTML.StringFromElement(html)
	# Summary
	summary = GetSummary(content)
	thumb = GetThumb(html)
	items = GetSourceLinks(html, type, quality)
	
	if len(items) == 0:
		return ObjectContainer(header=title, message=L('SourceWarning'))

	links = []

	OPR = ''

	for item in items:
		
		try:
			# Video site
			videosite = item.xpath("./text()")[0]
			#Log("Video Site: " + videosite)
			# Video link
			link = item.xpath("./@href")[0]
			if link.startswith("http") == False:
				link = link.lstrip('htp:/')
				link = 'http://' + link
			if len(links) > 1 and link.find('Part 1') != -1:
				break
			# Show date
			date = GetShowDate(videosite)
			# Get video source url and thumb
			link = common_fnc.GetTvURLSource(link,url,date,key=key)
			#Log("Video Site: " + videosite + " Link: " + link + " Thumb: " + thumb)
			if 'openload.' in link and Prefs['use_openload_pairing'] and OPR == '':
				if common_fnc.isOpenLoadPairingDone():
					OPR = ' *Paired*'
				else:
					OPR = ' *Pairing Required*'
		except:
			continue
			
		try:
			originally_available_at = Datetime.ParseDate(date).date()
		except:
			originally_available_at = ''

		# Add the found item to the collection
		if common_fnc.IsArrayItemInString2(common.VALID_SOURCES_DOMAIN, link, False) or (Prefs['allow_unknown_sources'] and URLService.ServiceIdentifierForURL(link) <> None):
			if link.find('openload') != -1 and not common_fnc.is_uss_installed() and Prefs['use_openload_pairing'] == False:
				return MC.message_container('Error', 'UnSupportedServices.bundle Required')
			elif link.find('openload') != -1 and Prefs['use_openload_pairing'] == True:
				link = "desitelly://" + E(JSON.StringFromObject({"title": videosite, "urls": [link], "thumb": thumb, "use_openload_pairing": Prefs['use_openload_pairing']}))
				
			links.append(URLService.NormalizeURL(link))
			oc.add(VideoClipObject(
				url = link, 
				title = '%s%s' % (videosite, OPR),
				thumb = Resource.ContentsOfURLWithFallback(thumb, fallback=R(ICON)),
				summary = summary,
				originally_available_at = originally_available_at))
	
	# If there are no channels, warn the user

	if len(oc) == 0 and 'disabled' in links:
		return ObjectContainer(header=title, message=L('DisabledWarning'))
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('SourceWarning'))

	return oc
	
####################################################################################################

def GetSourceLinks(html, key, key_qual):
	items = []
	if key_qual <> None:
		xpath_str = "//div[@class='content']//b[contains(font/text(),'"+key+" "+key_qual+"')]/following-sibling::a[count(. | //b[count(//b[contains(font/text(),'"+key+" "+key_qual+"')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font/text(),'"+key+" "+key_qual+"')]/preceding-sibling::b)+2]/preceding-sibling::a)]"
		#Log(xpath_str)
		items = html.xpath(xpath_str)
		if len(items) == 0:
			xpath_str = "//div[@class='content hasad']//b[contains(font[@color='Red']//text(), '"+key+" "+key_qual+"')]//following-sibling::a[count(. | //b[count(//b[contains(font[@color='Red']/text(),'"+key+" "+key_qual+"')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font[@color='Red']/text(),'"+key+" "+key_qual+"')]/preceding-sibling::b)+2]/preceding-sibling::a)]"
			#Log(xpath_str)
			items = html.xpath(xpath_str)
		if len(items) == 0:
			xpath_str = "//div[@class='content hasad']//b[contains(font[@color='Red']//text(), 'Watch Online - "+key+"')]//following-sibling::a[count(. | //b[count(//b[contains(font[@color='Red']/text(),'"+key+"')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font[@color='Red']/text(),'"+key+"')]/preceding-sibling::b)+2]/preceding-sibling::a)]"
			#Log(xpath_str)
			items = html.xpath(xpath_str)
		if len(items) == 0:
			xpath_str = "//div[@class='content hasad']//b[contains(font[@color='Red']//text(), '"+key+" "+key_qual+"')]//following-sibling::a"
			#Log(xpath_str)
			items = html.xpath(xpath_str)
	if len(items) == 0:
		if key_qual == None:
			xpath_str = "//div[@class='content hasad']//div[contains(font[@color='Red']//text(), '"+key+"')]//following-sibling::a"
		else:
			xpath_str = "//div[@class='content hasad']//div[contains(font[@color='Red']//text(), '"+key+" "+key_qual+"')]//following-sibling::a"
		#Log(xpath_str)
		items = html.xpath(xpath_str)
	return items

####################################################################################################

def GetMovieSources(html, key, isSplitParts=False):
	
	if not isSplitParts:
		try:
			xpath_str = ".//div[@class='content hasad']//b[contains(font[@color='Red']//text(), '"+key+"')][2]//following-sibling::a[position() >= 0 and position() < 2]"
			items = html.xpath(xpath_str)
			if len(items) > 0:
				return items
		except:
			items = []
	
	try:
		xpath_str = ".//div[@class='content hasad']//b[contains(font[@color='Red']//text(), '"+key+"')][1]//following-sibling::a[position() >= 0 and position() < 4]"
		items = html.xpath(xpath_str)
		if len(items) > 0:
			return items
	except:
		items = []
			
	return [key]
	
####################################################################################################

def GetOpenloadSources(html):
	items = html.xpath("//div[@class='content hasad']//b[contains(font[@color='Red']//text(), 'Watch Online - Openload')]//following-sibling::a[count(. | //b[count(//b[contains(font[@color='Red']/text(),'Openload')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font[@color='Red']/text(),'Openload')]/preceding-sibling::b)+2]/preceding-sibling::a)]")
	return items
	
def GetLetwatchusHD(html):
	items = html.xpath("//div[@class='content']//b[contains(font/text(),'Letwatch')]/following-sibling::a[count(. | //b[count(//b[contains(font/text(),'Letwatch')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font/text(),'Letwatch')]/preceding-sibling::b)+2]/preceding-sibling::a)]")
	if len(items) == 0:
		items = html.xpath("//div[@class='content hasad']//b[contains(font[@color='Red']//text(), 'Letwatch')]//following-sibling::a")
	return items

####################################################################################################

def GetLetwatchusDVD(html):
	items = html.xpath("//div[@class='content']//b[contains(font/text(),'Letwatch DVD')]/following-sibling::a[count(. | //b[count(//b[contains(font/text(),'Letwatch DVD')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font/text(),'Letwatch DVD')]/preceding-sibling::b)+2]/preceding-sibling::a)]")
	if len(items) == 0:
		items = html.xpath("//div[@class='content hasad']//b[contains(font[@color='Red']//text(), 'Letwatch DVD')]//following-sibling::a")
	return items
####################################################################################################

def GetDailymotion(html):
	items = html.xpath("//div[@class='content']//b[contains(font/text(),'DailyMotion')]/following-sibling::a[count(. | //b[count(//b[contains(font/text(),'DailyMotion')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font/text(),'DailyMotion')]/preceding-sibling::b)+2]/preceding-sibling::a)]")
	return items

####################################################################################################

def GetDailymotionHD(html):
	items = html.xpath("//div[@class='content']//b[contains(font/text(),'Dailymotion 720p')]/following-sibling::a[count(. | //b[count(//b[contains(font/text(),'Dailymotion 720p')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font/text(),'Dailymotion 720p')]/preceding-sibling::b)+2]/preceding-sibling::a)]")
	if len(items) == 0:
		items = html.xpath("//div[@class='content hasad']//b[contains(font[@color='Red']//text(), 'Dailymotion 720p')]//following-sibling::a")
	return items

####################################################################################################

def GetDailymotionDVD(html):
	items = html.xpath("//div[@class='content hasad']//b[contains(font[@color='Red']//text(), 'Dailymotion DVD')]//following-sibling::a")
	if len(items) == 0:
		items = html.xpath("//div[@class='content']//b[contains(font/text(),'Dailymotion DVD')]/following-sibling::a[count(. | //b[count(//b[contains(font/text(),'Dailymotion DVD')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font/text(),'Dailymotion DVD')]/preceding-sibling::b)+2]/preceding-sibling::a)]")
	return items
	
####################################################################################################

def GetDailymotionSD(html):
	items = html.xpath("//div[@class='content']//font[contains(./text(),'Dailymotion Links')]/following-sibling::a[count(. | //font[count(//font[contains(./text(),'Dailymotion Links')]/preceding-sibling::font)+2]/preceding-sibling::a) = count(//font[count(//font[contains(./text(),'Dailymotion Links')]/preceding-sibling::font)+2]/preceding-sibling::a)]")
	
	if len(items) == 0:
		items = html.xpath("//div[@class='content']//b[contains(./font/text(),'Dailymotion Links')]/following-sibling::a[count(. | //b[count(//b[contains(./font/text(),'Dailymotion Links')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(./font/text(),'Dailymotion Links')]/preceding-sibling::b)+2]/preceding-sibling::a)]")
	
	return items
	
####################################################################################################

def GetFlashPlayer(html):
	items = html.xpath("//div[@class='content']//b[contains(font/text(),'Flash Player')]/following-sibling::a[count(. | //b[count(//b[contains(font/text(),'Flash Player')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font/text(),'Flash Player')]/preceding-sibling::b)+2]/preceding-sibling::a)]")
	return items

####################################################################################################

def GetFlashPlayerHD(html):
	items = html.xpath("//div[@class='content']//b[contains(font/text(),'Flash Player 720p') or contains(font/text(),'Flash 720p')]/following-sibling::a[count(. | //b[count(//b[contains(font/text(),'Flash Player 720p') or contains(font/text(),'Flash 720p')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font/text(),'Flash Player 720p') or contains(font/text(),'Flash 720p')]/preceding-sibling::b)+2]/preceding-sibling::a)]")
	return items

####################################################################################################

def GetFlashPlayerDVD(html):
	items = html.xpath("//div[@class='content']//b[contains(font/text(),'Flash Player DVD') or contains(font/text(),'Flash DVD')]/following-sibling::a[count(. | //b[count(//b[contains(font/text(),'Flash Player DVD') or contains(font/text(),'Flash DVD')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font/text(),'Flash Player DVD') or contains(font/text(),'Flash DVD')]/preceding-sibling::b)+2]/preceding-sibling::a)]")
	return items

####################################################################################################

def GetMoviePostDate(html):
	# Get date
	date = html.xpath("//span[@class='date']/text()")[0]
	date = date.strip().replace(',','',1)
	#Log ("html date: " + str(date))
	# strip date to struct
	if date == 'Today':
		date = time.strftime('%Y%m%d', time.gmtime())
		#Log ("today: " + str(date))
	elif date == 'Yesterday':
		date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
		#Log ('yesterday: ' + str(date))
	else:
		date = time.strptime(date, '%m-%d-%Y')
		date = time.strftime('%Y%m%d', date)
	#Log ('Date: ' + str(date))
	return date

####################################################################################################

def GetShowDate(title):
	# find the date in the show title
	match = re.search(r'\d{1,2}[thsrdn]+\s\w+\s?\d{4}', title)
	#Log ('date match: ' + match.group())
	# remove the prefix from date
	match = re.sub(r'(st|nd|rd|th)', "", match.group(), 1)
	#Log ('remove prefix from match: ' + match)
	# add space between month and year
	match = re.sub(r'(\d{1,2}\s\w+)(\d{4})', r'\1 \2', match)
	#Log ('add space to month and year match: ' + match)
	# strip date to struct
	date = time.strptime(match, '%d %B %Y')
	# convert date
	date = time.strftime('%Y%m%d', date)
	#Log ('Final Date: ' + date)
	return date

####################################################################################################

def GetSummary(html):
	try:
		summary = html.xpath("//div[@class='content']//font[@size='3']/font/text()")[0]
		summary = summary.replace(" preview: ","",1)
		summary = summary.replace("Find out in","",1)
	except:
		summary = None
	return summary

####################################################################################################

def GetThumb(html):
	try:
		thumb = html.xpath("//ul[@class='singlecontent']/li/p/img/@src")[0]
		#Log ('Thumb: ' + thumb)
	except:
		thumb = R(ICON)
	return thumb

####################################################################################################