import common, urllib2, redirect_follower, json, re
import desitvbox, desitashan, desirulez

global_request_timeout = 10

GOOD_RESPONSE_CODES = ['200','206']

BANNED_KEYWORDS = ['File Does not Exist','Has Been Removed','Content removed','Content rejected','Content removed','Content rejected','This video got removed','File was deleted','We are sorry','copyright violation','File Not Found']

MC = common.NewMessageContainer(common.PREFIX, common.TITLE)

####################################################################################################
# Get HTTP response code (200 == good)
@route(common.PREFIX + '/gethttpstatus')
def GetHttpStatus(url):
	try:
		conn = urllib2.urlopen(url, timeout = global_request_timeout)
		resp = str(conn.getcode())
	except StandardError:
		resp = '0'
	#Log(url +' : HTTPResponse = '+ resp)
	return resp
	

####################################################################################################
# Get HTTP response code (200 == good)
@route(common.PREFIX + '/followredirectgethttpstatus')
def FollowRedirectGetHttpStatus(url):
	try:
		response = GetRedirectingUrl(url, url)
		if response <> None:
			resp = str(response.getcode())
	except:
		resp = '0'
	#Log(url +' : HTTPResponse = '+ resp)
	return resp
		
####################################################################################################
# Gets the redirecting url 
@route(common.PREFIX + '/getredirectingurl')
def GetRedirectingUrl(url, rurl):

	#Log("Url ----- : " + url)
	redirectUrl = url
	try:
		response = redirect_follower.GetRedirect(url, rurl, global_request_timeout)
		if response <> None:
			redirectUrl = response.geturl()
	except:
		redirectUrl = url
			
	#Log("Redirecting url ----- : " + redirectUrl)
	return redirectUrl

####################################################################################################
# checks if USS is installed or not
def is_uss_installed():
    """Check install state of UnSupported Services"""

    identifiers = list()
    plugins_list = XML.ElementFromURL('http://127.0.0.1:32400/:/plugins', cacheTime=0)

    for plugin_el in plugins_list.xpath('//Plugin'):
        identifiers.append(plugin_el.get('identifier'))

    if 'com.plexapp.system.unsupportedservices' in identifiers:
        return True
    return False
	
####################################################################################################
# search array item's presence in string
@route(common.PREFIX + "/isarrayiteminstring")
def IsArrayItemInString(arr, mystr, case_match=True, exact=False):

	for item in arr:
		if not case_match:
			item = item.lower()
			mystr = mystr.lower()
		if exact:
			if item == mystr and mystr.startswith(item):
				return True
		else:
			if item in mystr and mystr.startswith(item):
				return True
			
	return False
	
####################################################################################################
# search array item's presence in string
@route(common.PREFIX + "/isarrayiteminstring")
def IsArrayItemInString2(arr, mystr, case_match=True):

	for item in arr:
		if case_match == False:
			item = item.lower()
			mystr = mystr.lower()
		if item in mystr:
			#Log('-------------------' + item)
			return True
			
	return False
	
####################################################################################################
# search array item's presence in string
@route(common.PREFIX + "/getarrayitemmatchinstring")
def GetArrayItemMatchInString(arr, mystr, case_match=True, exact=False):

	c=-1
	#Log('-------------------' + mystr)
	for item in arr:
		#Log('-------------------' + item)
		c=c+1
		if case_match == False:
			item = item.lower()
			mystr = mystr.lower()
		if exact:
			if item == mystr:
				return item, c
		else:
			if item in mystr:
				return item, c
			
	return (None, -1)

####################################################################################################	
def GetTvURLSource(url, referer, date='', key=None):

	#Log(url)
	# This will take care of Meta redirects
	url = GetRedirectingUrl(url, url)
	#Log(url)
	html = HTML.ElementFromURL(url=url, headers={'Referer': referer})
	string = HTML.StringFromElement(html)

	try:
		if string.find('dailymotion.com') != -1:
			#Log('dailymotion')
			url = html.xpath("//iframe[contains(@src,'dailymotion')]/@src")[0]
		elif string.find('vmg.') != -1:
			#Log('vmg')
			url = html.xpath("//iframe[contains(@src,'vmg.')]/@src")[0]
		elif string.find('vidshare.') != -1:
			#Log('vidshare')
			url = html.xpath("//iframe[contains(@src,'vidshare.')]/@src")[0]
		elif string.find('cloudy.ec') != -1:
			#Log('cloudy')
			url = html.xpath("//iframe[contains(@src,'cloudy')]/@src")[0]
		elif string.find('playwire.com') != -1:
			#Log('playwire')
			url = html.xpath("//script/@data-config")[0]
		elif string.find('playu.') != -1:
			#Log('playu')
			url = html.xpath("//iframe[contains(@src,'playu.')]/@src")[0]
		elif len(html.xpath("//iframe[contains(@src,'openload.')]/@src")) > 0:
			#Log('openload')
			url = html.xpath("//iframe[contains(@src,'openload.co')]/@src")[0]
		elif string.find('tune.pk') != -1:
			#Log('tune')
			try:
				url = html.xpath("//script[contains(@src,'tune.')]/@src")[0]
			except:
				url = html.xpath("//iframe[contains(@src,'tune.')]/@src")[0]
				html = HTML.ElementFromURL(url=url, headers={'Referer': url})
				url = html.xpath("//iframe[contains(@src,'tune.')]/@src")[0]
				
			if 'load.js' in url:
				url = 'https://tune.pk/player/embed_player.php?vid=%s&folder=&width=595&height=430&autoplay=no' % re.findall(r'vid=(.*?)&', url)[0]
				html = HTML.ElementFromURL(url=url, headers={'Referer': url})
				url = html.xpath("//iframe[contains(@src,'tune.')]/@src")[0]
		else:
			#Log('Undefined src')
			orig_url = url
			if key <> None:
				url = html.xpath("//iframe[contains(@src,'"+key+"')]/@src")
				if len(url) > 0:
					url = url[0]
				else:
					url = orig_url
			if orig_url == url:
				url = html.xpath("//iframe[contains(@src,'embed')]/@src")
				if len(url) > 0:
					url = url[0]
				else:
					url = orig_url
			if orig_url == url:
				url = html.xpath(".//iframe//@src")
				if len(url) > 0:
					url = url[0]
					url = GetTvURLSource(url,url,date)
				else:
					url = orig_url
			if orig_url == url:
				url = 'none'
			else:
				referer = orig_url
	except:
		pass
		
	if Prefs["use_debug"]:
		Log("common_fnc.GetTvURLSource : %s" % url)
		
	if url.startswith('//'):
		url = 'http:' + url
		
	url = CheckURLSource(url=url, referer=referer, key=key, string=string, html=html)
	
	if Prefs["use_debug"]:
		Log("Post CheckURLSource-a")
		Log("common_fnc.GetTvURLSource : %s" % url)
		
	if 'watchvideo18.' in url:
		url = "watchvideo://" + E(JSON.StringFromObject({"url": url}))
	elif 'vidwatch.' in url:
		url = "vidwatch://" + E(JSON.StringFromObject({"url": url}))
		
	if Prefs["use_debug"]:
		Log("Post CheckURLSource-b")
		Log("common_fnc.GetTvURLSource : %s" % url)

	return url

####################################################################################################	
def CheckURLSource(url, referer, key=None, string=None, html=None, stringMatch=False):

	if string == None:
		string = HTTP.Request(url=url, headers={'Referer': referer}).content
		
	page = None
	try:
		if string.find('dailymotion.com') != -1:
			#Log('dailymotion')
			page = HTTP.Request(url, headers={'Referer': referer}).content
			if 'Content removed' in page or 'Content rejected' in page:
				url = 'disabled'
		elif string.find('vmg.') != -1:
			#Log('vmg')
			page = HTTP.Request(url, headers={'Referer': referer}).content
			if 'Content removed' in page or 'Content rejected' in page or 'This video got removed' in page or 'ERROR' in page:
				url = 'disabled'
		elif string.find('thevideobee.') != -1:
			#Log('vmg')
			page = HTTP.Request(url, headers={'Referer': referer}).content
			if 'no longer available' in page or 'has been deleted' in page:
				url = 'disabled'
			elif 'Video encoding error' in page:
				url = 'errored'
		elif string.find('tune.') != -1:
			#Log('tune')
			page = HTTP.Request(url, headers={'Referer': referer}).content
			if 'Content removed' in page or 'Content rejected' in page or 'this video has been deactivated' in page or 'ERROR' in page:
				url = 'disabled'
		elif string.find('vidshare.') != -1:
			#Log('vidshare')
			try:
				page = HTML.ElementFromURL(url, headers={'Referer': referer})
				img = page.xpath("//img/@src")
				if len(img) == 0:
					url = 'disabled'
			except:
				url = 'disabled'
		elif string.find('cloudy.ec') != -1:
			#Log('cloudy')
			if not isValidCloudyURL(url):
				url = 'disabled'
		elif string.find('playwire.com') != -1:
			#Log('playwire')
			page = JSON.ObjectFromURL(url, headers={'Referer': referer})
			try:
				disabled = page['disabled']['message']
				if 'disabled' in disabled:
					url = 'disabled'
			except:
				pass
		elif string.find('playu.') != -1:
			#Log('playu')
			page = HTTP.Request(url, headers={'Referer': referer}).content
			if 'File was deleted' in page:
				url = 'disabled'
		elif (html <> None and len(html.xpath("//iframe[contains(@src,'openload.')]/@src")) > 0) and (stringMatch and string.find('openload.') != -1):
			#Log('openload')
			page = HTTP.Request(url, headers={'Referer': referer}).content
			if 'We are sorry' in page or 'copyright violation' in page:
				url = 'disabled'
		else:
			#Log('Testing Undefined src')
			if url <> 'none':
				page = HTTP.Request(url, headers={'Referer': referer}).content
				#Log(page)
				if IsArrayItemInString2(BANNED_KEYWORDS, page, False):
					url = 'disabled'
					break
		#Log(page)
		if page != None and '/dot/' in page:
			url = 'dot_blocked'
	except:
		pass

	return url
	
####################################################################################################

def isValidCloudyURL(url):
		
	vurl = False
	try:
		# use api www.cloudy.ec/api/player.api.php?'user=undefined&pass=undefined&file={file}&key={key}
		# https://github.com/Eldorados/script.module.urlresolver/blob/master/lib/urlresolver/plugins/cloudy.py
		
		content = unicode(HTTP.Request(url).content)
		elems = HTML.ElementFromString(content)
		key = elems.xpath("substring-before(substring-after(//script[@type='text/javascript'][3]//text(),'key: '),',')").replace("\"",'')
		file = elems.xpath("substring-before(substring-after(//script[@type='text/javascript'][3]//text(),'file:'),',')").replace("\"",'')
		
		furl = "http://www.cloudy.ec/api/player.api.php?'user=undefined&pass=undefined&file="+file+"&key="+key
		
		content = unicode(HTTP.Request(furl).content)
		#Log(vurl)
		if 'error' not in content:
			vurl = True
	except:
		vurl = False
		
	#Log("bool --------" + str(vurl))
	return vurl
	
	
openloadhdr = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	'Accept-Encoding': 'none',
	'Accept-Language': 'en-US,en;q=0.8',
	'Connection': 'keep-alive'}
	
API_URL = 'https://api.openload.co/1'
PAIR_INFO_URL = API_URL + '/streaming/info'
GET_VIDEO_URL = API_URL + '/streaming/get?file=%s'
VALID_URL = r'https?://(?:openload\.(?:co|io)|oload\.tv)/(?:f|embed)/(?P<id>[a-zA-Z0-9-_]+)'

def matchOpenLoadID(url):
	VALID_URL_RE = re.compile(VALID_URL)
	m = VALID_URL_RE.match(url)
	assert m
	return m.group('id')

def isOpenLoadPairingDone():
	
	pairurl = 'https://openload.co/pair'
	echourl = 'https://v4speed.oloadcdn.net/echoip'
	checkpairurl = 'https://openload.co/checkpair/%s'
	
	r = HTTP.Request(echourl).content
	print "URL:%s  Resp:%s" % (echourl, r)
	
	checkpairurl_withip = checkpairurl % r
	r = HTTP.Request(checkpairurl_withip).content
	
	if r != None and '1' in r:
		return True
		
	return False
	
def pairing_method_OpenLoad(url):
	
	video_id = matchOpenLoadID(url)
	
	get_info = HTTP.Request(GET_VIDEO_URL % video_id, headers=openloadhdr).content
	#print "get_info --- %s" % get_info
	get_info = json.loads(get_info)
	status = get_info.get('status')
	#print "status --- %s" % status
	if status == 200:
		result = get_info.get('result', {})
		return result.get('url')
	elif status == 403:
		pair_info = HTTP.Request(PAIR_INFO_URL, headers=openloadhdr).content
		#print "pair_info --- %s" % pair_info
		pair_info = json.loads(pair_info)
		if pair_info.get('status') == 200:
			pair_url = pair_info.get('result', {}).get('auth_url')
			if pair_url:
				#print 'Open this url: %s, solve captcha, click "Pair" button and try again' % pair_url
				Log('Open this url: %s, solve captcha, click "Pair" button and try again' % pair_url)
			else:
				#print 'Pair URL not found'
				Log('Pair URL not found: %s' % video_id)
		else:
			#print 'Error loading pair info'
			Log('Error loading pair info: %s' % video_id)
	else:
		#print 'Error loading JSON metadata'
		msg = get_info.get('msg')
		Log('Error %s - %s: %s' % (status, msg, video_id))
		
	return None
	
######### PINS #############################################################################
# Checks a show to the Pins list using the url as a key
@route(common.PREFIX + "/checkpin")	
def CheckPin(url):

	bool = False
	url = Dict['Plex-Pin-Pin'+url]
	if url <> None and url <> 'removed':
		bool = True
	return bool

######################################################################################
# Adds a Channel to the Pins list using the url as a key
@route(common.PREFIX + "/addpin")
def AddPin(site, title, url):
	
	Dict['Plex-Pin-Pin'+url] = site + 'Key4Split' + title + 'Key4Split' + url
	Dict.Save()
	return ObjectContainer(header = title, message='This Show has been added to your Pins.', title1='Pin Added')

######################################################################################
# Removes a Channel from the Pins list using the url as a key
@route(common.PREFIX + "/removepins")
def RemovePin(url):
	
	title = 'Undefined'
	keys = Dict['Plex-Pin-Pin'+url]
	if 'Key4Split' in keys:
		values = keys.split('Key4Split')
		title = values[1]
		Dict['Plex-Pin-Pin'+url] = None
		Dict.Save()
	return ObjectContainer(header=title, message='This Show has been removed from your Pins.', title1='Pin Removed')	

######################################################################################
# Clears the Dict that stores the Pins list	
@route(common.PREFIX + "/clearpins")
def ClearPins():

	for each in Dict:
		keys = Dict[each]
		if keys <> None and 'Key4Split' in str(keys):
			Dict[each] = None
	Dict.Save()
	return ObjectContainer(header="My Pins", message='Your Pins list will be cleared soon.', title1='Pins Cleared')
	
######################################################################################
# Pins
@route(common.PREFIX + "/pins")	
def Pins(title):

	oc = ObjectContainer(title1 = title)
	
	for each in Dict:
		try:
			keys = Dict[each]
			#Log("keys--------- " + str(keys))
			if keys <> None and 'Key4Split' in str(keys):
				values = keys.split('Key4Split')
				site = values[0]
				title = values[1]
				channelUrl = values[2]

				if site == desitvbox.SITETITLE:
					oc.add(DirectoryObject(key = Callback(desitvbox.EpisodesMenu, url = channelUrl, title = title), title = title, thumb = R(desitvbox.SITETHUMB)))
				elif site == desitashan.SITETITLE:
					oc.add(DirectoryObject(key = Callback(desitashan.EpisodesMenu, url = channelUrl, title = title), title = title, thumb = R(desitashan.SITETHUMB)))
				elif site == desirulez.SITETITLE:
					oc.add(DirectoryObject(key = Callback(desirulez.EpisodesMenu, url = channelUrl, title = title), title = title, thumb = R(desirulez.SITETHUMB)))
		except:
			pass
			
	if len(oc) == 0:
		return ObjectContainer(header='Pins', message='No Pinned Shows Available', title1='Pins Unavailable')
	
	oc.objects.sort(key=lambda obj: obj.title)
	#add a way to clear pin list
	oc.add(DirectoryObject(
		key = Callback(ClearPins),
		title = "Clear All Pins",
		thumb = R(common.ICON_PIN),
		summary = "CAUTION! This will clear your entire Pins list!"
		)
	)

	return oc
	
####################################################################################################
@route(common.PREFIX + "/MyMessage")
def MyMessage(title, msg, **kwargs):	
	return MC.message_container(title,msg)