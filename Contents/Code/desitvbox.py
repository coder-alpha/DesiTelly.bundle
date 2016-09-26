import common, common_fnc
import re
import time
import datetime
import messages

SITETITLE = 'DesiTvBox'
SITEURL = 'http://www.desitvbox.me/'
SITETHUMB = 'icon-desitvbox.png'

PREFIX = common.PREFIX
NAME = common.NAME
ART = common.ART
ICON = common.ICON

MC = messages.NewMessageContainer(common.PREFIX, common.TITLE)

####################################################################################################

@route(PREFIX + '/desitvbox/channels')
def ChannelsMenu(url):
	oc = ObjectContainer(title2=SITETITLE)

	html = HTML.ElementFromURL(url)

	for item in html.xpath("//nav[@class='site_navigation']//a"):
		try:
			# Channel title
			channel = item.xpath("text()")[0]

			# Channel link
			link = item.xpath("@href")[0]
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

@route(PREFIX + '/desitvbox/showsmenu')
def ShowsMenu(url, title):
	oc = ObjectContainer(title2=title)

	html = HTML.ElementFromURL(url)
	
	for item in html.xpath("//div[@class='entry_content']//li//a"):
		try:
			# Show title
			show = item.xpath("text()")[0]
			
			# Show link
			link = item.xpath("@href")[0]
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

@route(PREFIX + '/desitvbox/episodesmenu')
def EpisodesMenu(url, title):
	oc = ObjectContainer(title2 = unicode(title))

	pageurl = url

	html = HTML.ElementFromURL(pageurl)
	
	for item in html.xpath("//div[@class='col main-content col_9_of_12']//div[@class='item_content']//h4//a"):
		try:
			# Episode title
			episode = unicode(str(item.xpath("text()")[0].strip()))
			
			# episode link
			link = item.xpath("@href")[0]
			if link.startswith("http") == False:
				link = SITEURL + link
			#Log("Episode: " + episode + " Link: " + link)
		except:
			continue

		# Add the found item to the collection
		if 'Watch Online' in episode:
			oc.add(PopupDirectoryObject(key=Callback(PlayerLinksMenu, url=link, title=episode, type=L('Tv')), title=episode))
	
	# Find the total number of pages
	pages = ' '
	try:
		pages = html.xpath("//div[@class='col main-content col_9_of_12']//ul[@class='page-numbers']//a[@class='next page-numbers']//@href")[0]
	except:
		pass
			
	# Add the next page link if exists
	if ' ' not in pages:
		oc.add(DirectoryObject(key=Callback(EpisodesMenu, url=pages, title=title), title=L('Pages')))
	
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

@route(PREFIX + '/desitvbox/playerlinksmenu')
def PlayerLinksMenu(url, title, type):
	oc = ObjectContainer(title2 = unicode(title))
	
	# Add the item to the collection
	html = HTML.ElementFromURL(url=url, headers={'Referer': url})
	content = HTML.StringFromElement(html)
	
	if 'http://www.desitvbox.me/images/coming.png' in content:
		return ObjectContainer(header=title, message=L('ComingSoonWarning'))
	
	sources = html.xpath(".//div[@class='col main-content col_9_of_12']//p[contains(.//text(),' HD')]//text()")
	if len(sources) == 0:
		sources = html.xpath(".//div[@class='col main-content col_9_of_12']//p[contains(.//text(),'Watch Online')]//text()")

	for source in sources:
		s_source, i = common_fnc.GetArrayItemMatchInString(common.VALID_SOURCES, source, False)
		if s_source <> None:
			if '720p' in source.lower():
				if 'single' in source.lower():
					oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source), title=(common.VALID_SOURCES[i] + ' HD (Single Link)'), thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
				else:
					oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source), title=(common.VALID_SOURCES[i] + ' HD'), thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
			elif 'hd' in source.lower():
				oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source), title=(common.VALID_SOURCES[i] + ' HD'), thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
			elif 'dvd' in source.lower():
				oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source), title=(common.VALID_SOURCES[i] + ' DVD'), thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
			else:
				oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source), title=common.VALID_SOURCES[i], thumb=R('icon-'+common.VALID_SOURCES_ICONS[i]+'.png')))
		elif Prefs['allow_unknown_sources']:
			oc.add(DirectoryObject(key=Callback(EpisodeLinksMenu, url=url, title=title, type=source), title=source, thumb=R('icon-unknown.png')))

	# If there are no channels, warn the user
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('PlayerWarning'))

	return oc

####################################################################################################

@route(PREFIX + '/desitvbox/episodelinksmenu')
def EpisodeLinksMenu(url, title, type):
	oc = ObjectContainer(title2 = unicode(title))

	html = HTML.ElementFromURL(url)
	
	# Summary
	summary = GetSummary(html)
	videosite = ''
	thumb = GetThumb(url)
	oc.art = Resource.ContentsOfURLWithFallback(thumb, fallback=R(ART))
	
	originally_available_at = ''
	items = GetParts(html, type)
	bool_do_use_parts_feature = True
	links = []

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
			#Log("link: " + link)
			# Show date
			date = GetShowDate(videosite)
			#Log("date: " + date)
			# Get video source url and thumb
			link = common_fnc.GetTvURLSource(link,url,date)
			Log("Video Site: " + videosite + " Link: " + link + " Thumb: " + thumb)
		except:
			continue
			
		try:
			originally_available_at = Datetime.ParseDate(date).date()
		except:
			originally_available_at = ''
			
		links.append(link)
		
		# Add the found item to the collection
		if common_fnc.IsArrayItemInString2(common.VALID_SOURCES_DOMAIN, link, False) or (Prefs['allow_unknown_sources'] and URLService.ServiceIdentifierForURL(link) <> None):
		
			if link.find('openload') != -1 and not common_fnc.is_uss_installed():
				return MC.message_container('Error', 'UnSupportedServices.bundle Required')

			if not Prefs['consolidate_parts'] or (link.find('playwire.') == -1 and Prefs['consolidate_parts']):
				bool_do_use_parts_feature = False
				oc.add(VideoClipObject(
					url = link,
					title = videosite,
					art = Resource.ContentsOfURLWithFallback(thumb, fallback=R(ART)),
					thumb = Resource.ContentsOfURLWithFallback(thumb, fallback=R(ICON)),
					summary = summary,
					originally_available_at = originally_available_at))
					
					
	if Prefs['consolidate_parts'] and bool_do_use_parts_feature and len(links) > 0 and 'disabled' not in links:
		videosite = unicode(str(videosite).split('– Part')[0].strip() + ' - ' + str(len(links)) + ' Parts')
		oc.add(VideoClipObject(
            title = videosite,
            thumb = Resource.ContentsOfURLWithFallback([thumb, R(ICON)]),
			art = Resource.ContentsOfURLWithFallback([thumb,R(ART)]),
			summary = summary,
			originally_available_at = originally_available_at,
            url="desitelly://" + E(JSON.StringFromObject({"title": videosite, "urls": links, "thumb": thumb}))
            ))
	
	# If there are no channels, warn the user
	if len(oc) == 0 and 'disabled' in links:
		return ObjectContainer(header=title, message=L('DisabledWarning'))
	if len(oc) == 0:
		return ObjectContainer(header=title, message=L('SourceWarning'))

	return oc

####################################################################################################

def GetParts(html, keyword):
	items = html.xpath(".//div[@class='col main-content col_9_of_12']//p[contains(b//text(),'"+keyword+"')]//following-sibling::p[1]//a")
	if len(items) == 0:
		items = html.xpath(".//div[@class='col main-content col_9_of_12']//p[contains(span//text(),'"+keyword+"')]//following-sibling::p[1]//a")
	if len(items) == 0:
		items = html.xpath(".//div[@class='col main-content col_9_of_12']//p//a[contains(b//text(),'"+keyword+"')]//parent::node()//following-sibling::p[1]//a")
	if len(items) == 0:
		items = html.xpath(".//div[@class='col main-content col_9_of_12']//p[contains(.//text(),'"+keyword+"')]//following-sibling::p[1]//a")
		
	return items

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

def GetThumb(url):
	try:
		html = HTML.ElementFromURL(url)
		thumb = html.xpath("//ul[@class='singlecontent']/li/p/img/@src")[0]
		#Log ('Thumb: ' + thumb)
	except:
		thumb = ''
	return thumb