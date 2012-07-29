#nosOS2012.bundle VideoPlugin v1.0.0
#Created by Matthijs Drenth

import sys
import urllib 
import re

####################################################################################################

VIDEO_PREFIX = "/video/nosOS2012"

NAME = 'Olympische Spelen 2012'

ART  = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################

def Start():

    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup("PanelStream", viewMode="PanelStream", mediaType="items")
    

    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "List"
    MediaContainer.art = R(ART)
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)
    
    HTTP.CacheTime = 1
	

####################################################################################################

def VideoMainMenu():

	dir = MediaContainer(viewGroup="PanelStream")
	url ='http://nos.nl/os2012/wedstrijdschema/'
	itemnr = 00
	for item in HTML.ElementFromURL(url).xpath('//*[@id="os-videoplayer"]/div/div[2]/ol/li'):
		itemnr = itemnr + 01

		
		if itemnr > 1:
			channel = item.xpath('a/h3/em')[0].text
			watch = item.xpath('p[1]')[0].text
			next = item.xpath('//p[@class="later"]')[0].text
			sport = item.xpath('a/h3')[0].get('data-sport-name')
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
				
		dir.Append(Function(VideoItem(GetUrl, title=title, summary=summary, subtitle=None, thumb=None), url=channel, title=title))
	return dir

####################################################################################################


def GetUrl(sender, url, title):
	url = 'plex://localhost/video/:/webkit?url=http://nos.nl/os2012/play/' + url +'/'
	return Redirect(url)
		
####################################################################################################

def GetThumb(vl):
	sock = urllib.urlopen(vl) 
	pagecontent = sock.read()                            
	sock.close()
	
	m2 = re.search('mp4_file=(.{0,})(_ipad.mp4\")', pagecontent)
	thumb = m2.group(1)
	thumb = "http://media.autoweek.nl/m/" + thumb + "_m.jpg"
	try:
		image = HTTP.Request(thumb, cacheTime=CACHE_1MONTH).content
		return DataObject(image, 'image/jpeg')
	except:
		return Redirect(R(PLUGIN_ICON_DEFAULT))
		
####################################################################################################