#nosOS2012.bundle VideoPlugin v1.0.1
#Created by Matthijs Drenth

import urllib 

####################################################################################################

VIDEO_PREFIX = "/video/nosOS2012"

NAME = 'Olympische Spelen 2012'

ART  = 'art-default.jpg'
ICON = 'icon-default.png'
BASE_URL = 'http://nos.nl/os2012'

####################################################################################################

def Start():

    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup("PanelStream", viewMode="PanelStream", mediaType="items")
	
	MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "InfoList"
    MediaContainer.art = R(ART)
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)
    
    HTTP.CacheTime = 1
	

####################################################################################################

def VideoMainMenu():
	dir = MediaContainer(viewGroup="InfoList")
	url = BASE_URL + '/wedstrijdschema/'
	itemnr = 00
	for item in HTML.ElementFromURL(url).xpath('//div[@class="channels"]/ol/li'):
		itemnr = itemnr + 01
		if itemnr > 1:
			channel = item.xpath('a/h3/em')[0].text
			watch = item.xpath('p[1]')[0].text
			next = item.xpath('//p[@class="later"]')[0].text
			sport = item.xpath('a/h3')[0].get('data-sport-name').capitalize()
			until = item.xpath('a/div[@class="meta"]/span[@class="time"]')[0].text
		else:
			channel = '13'
			name = item.xpath('a/h3')[0].text
			sport = 'Nederland 1'
			watch = ''
			next = ''
			until = ''
			medal = ''
		title = sport + " - kanaal " + channel
		summary = "Nu: " + sport + " " + " "+ watch + " " + until + "\n\n" + next
		dir.Append(Function(VideoItem(GetUrl, title=title, summary=summary, subtitle=sport, thumb=None), view=channel))
	return dir

####################################################################################################

def GetUrl(sender, view):
	url = BASE_URL + '/play/' + view + '/'
	Log('opening : ' + url)
	### for v2 plugins ###
	return Redirect(WebVideoItem(url))
		
####################################################################################################