'''
    Current TV - XBMC music plugin

    Coding by queeup
    http://code.google.com/p/queeup/

    Credits:
        * Current TV               [http://current.com/]
        * Universal Feed Parser    [http://feedparser.org/]

    Changelog:
        v1.0.1 (20.10.2009)
        added: Next pages
'''

# Constants
import xbmcaddon
__addon__     = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__path__      = __addon__.getAddonInfo('path')
__author__    = __addon__.getAddonInfo('author')
__version__   = __addon__.getAddonInfo('version')

# Imports
import os
import re
import sys
import time
import xbmc
import xbmcgui
import xbmcplugin
import urllib

pluginhandle = int (sys.argv[1])

# Debug
if xbmcplugin.getSetting(pluginhandle, "debug") == "true":
    xbmc.log("[PLUGIN] '%s: version %s' initialized!" % (__addonname__, __version__,), xbmc.LOGNOTICE)

# Append Library and Image Directory
ROOT_DIR, LIB_DIR, IMG_DIR = (xbmc.translatePath(os.path.join(__path__, '')),
                              xbmc.translatePath(os.path.join(__path__, 'resources', 'lib')),
                              xbmc.translatePath(os.path.join(__path__, 'resources', 'img', '')))
sys.path.append(ROOT_DIR)
sys.path.append(LIB_DIR)
sys.path.append(IMG_DIR)

# Fanart
xbmcplugin.setPluginFanart(pluginhandle, IMG_DIR + 'fanart.png')

# Parser
import feedparser

#  -----------------------------------------------------------------------------
def MAIN():
    Main = [{'title':'Currency', 'thumb':'currency.png', 'url':'http://feeds.current.com/groups/currency.rss?page=%u', 'genre':'Other'},
            {'title':'Current Edge', 'thumb':'currentedge.png', 'url':'http://feeds.current.com/groups/current-edge.rss?page=%u', 'genre':'Other'},
            {'title':'Current Fix', 'thumb':'currentfix.png', 'url':'http://feeds.current.com/groups/current-fix.rss?page=%u', 'genre':'Music'},
            {'title':'Current Ride', 'thumb':'currentride.png', 'url':'http://feeds.current.com/groups/current-ride.rss?page=%u', 'genre':''},
            {'title':'Current Tech', 'thumb':'currenttech.png', 'url':'http://feeds.current.com/groups/current-tech.rss?page=%u', 'genre':'Tech'},
            {'title':'Current Virals', 'thumb':'currentvirals.png', 'url':'http://feeds.current.com/groups/current-virals.rss?page=%u', 'genre':'Comedy'},
            {'title':'Daily Fix', 'thumb':'dailyfix.png', 'url':'http://feeds.current.com/groups/daily-fix.rss?page=%u', 'genre':'Music'},
            {'title':'Infomania', 'thumb':'infomania.png', 'url':'http://feeds.current.com/groups/infomania.rss?page=%u', 'genre':'News'},
            {'title':'Joe Central', 'thumb':'joe.png', 'url':'http://feeds.current.com/groups/joe-central.rss?page=%u', 'genre':'Comedy'},
            {'title':'Salon', 'thumb':'salon.png', 'url':'http://feeds.current.com/groups/salon.rss?page=%u', 'genre':'Other'},
            {'title':'Supernews', 'thumb':'supernews.png', 'url':'http://feeds.current.com/groups/supernews.rss?page=%u', 'genre':'Comedy'},
            {'title':'Vanguard Journalism', 'thumb':'vanguard.png', 'url':'http://feeds.current.com/groups/vanguard-journalism.rss?page=%u', 'genre':'News'},
            {'title':'Viewer Uploads', 'thumb':'uploads.png', 'url':'http://feeds.current.com/groups/vc2-us.rss?page=%u', 'genre':'Other'},
            {'title':'Make Commons Day', 'thumb':'', 'url':'http://feeds.current.com/groups/make-commons-day.rss?page=%u', 'genre':'Music'},
            {'title':'The Rotten Tomatoes Show', 'thumb':'rtshow.jpg', 'url':'http://feeds.current.com/groups/the-rotten-tomatoes-show.rss?page=%u', 'genre':'Movies'},
            {'title':'Embedded', 'thumb':'embedded.jpg', 'url':'http://feeds.current.com/groups/embedded.rss?page=%u', 'genre':'Music'},
            {'title':'White Hot Top 5', 'thumb':'whitehottop5.jpg', 'url':'http://feeds.current.com/groups/white-hot-top-5.rss?page=%u', 'genre':'Music'},
            {'title':'Microsoft VCAM', 'thumb':'microsoft.jpg', 'url':'http://feeds.current.com/groups/microsoft-vcam.rss?page=%u', 'genre':'Tech'},
            {'title':'Axe VCAM', 'thumb':'axe.jpg', 'url':'http://feeds.current.com/groups/axe-vcam.rss?page=%u', 'genre':'Other'},
            {'title':'Thats Gay', 'thumb':'thatsgay.jpg', 'url':'http://feeds.current.com/groups/thats-gay.rss?page=%u', 'genre':'Comedy'},
            {'title':'Target Women', 'thumb':'targetwomen.jpg', 'url':'http://feeds.current.com/groups/target-women.rss?page=%u', 'genre':'Comedy'},
            {'title':'Current Style', 'thumb':'', 'url':'http://feeds.current.com/groups/current-style.rss?page=%u', 'genre':'Art and Style'},
            {'title':'Current Look', 'thumb':'', 'url':'http://feeds.current.com/groups/current-look.rss?page=%u', 'genre':'Art and Style'}, ]
    for i in Main:
        listitem = xbmcgui.ListItem(i['title'], iconImage='DefaultFolder.png', thumbnailImage=IMG_DIR + i['thumb'])
        listitem.setInfo(type="Video",
                         infoLabels={"Title" : i['title'],
                                     "Label" : i['title'],
                                     "TVShowTitle" : i['title'],
                                     "Genre" : i['genre'],
                                     })
        url = '%s?mode=%i&url=%s&name=%s' % (sys.argv[0], 0, urllib.quote_plus(i['url'] % 1), i['title'])
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[ 1 ]), url=url, listitem=listitem, isFolder=True)
    # Content Type
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    # Sort methods and content type...
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
    # End of directory...
    xbmcplugin.endOfDirectory(handle=int(sys.argv[ 1 ]), succeeded=True)

def LIST(url, name, page):
    pageurl = url
    url = url.replace('page=1', '')
    if xbmcplugin.getSetting(pluginhandle, "debug") == "true":
        xbmc.log("[PLUGIN :%s]\nLIST(url):\nURL :%spage=%i\nNAME :%s" % (__addonname__, url, int(page), name))
    d = feedparser.parse(url + 'page=%i' % (int(page)))
    for entry in d.entries:
        title = entry.title
        link = entry.link.split('?')[0]
        thumb = entry.media_thumbnail[0]['url']
        date_p = entry.date_parsed
        date = time.strftime("%d.%m.%Y", date_p)
        desc = entry.media_description.strip()
        listitem = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage=thumb)
        listitem.setInfo(type="Video",
                             infoLabels={"Title" : title,
                                         "Label" : title,
                                         "Date" : date,
                                         "Plot" : desc
                                         })
        url = '%s?mode=%i&url=%s' % (sys.argv[0], 1, urllib.quote_plus(link))
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[ 1 ]), url=url, listitem=listitem, isFolder=False)
    # Next Page
    listitem = xbmcgui.ListItem('>>Next Page', iconImage='DefaultFolder.png', thumbnailImage=IMG_DIR + 'next.png')
    url = '%s?mode=%i&url=%s&page=%i&name=%s' % (sys.argv[0], 0, urllib.quote_plus(pageurl), int(page) + 1, name)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[ 1 ]), url=url, listitem=listitem, isFolder=True)
    # Content Type
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    # Sort methods and content type...
    xbmcplugin.addSortMethod(int(sys.argv[ 1 ]), 1)
    xbmcplugin.addSortMethod(int(sys.argv[ 1 ]), 3)
    # End of directory...
    xbmcplugin.endOfDirectory(handle=int(sys.argv[ 1 ]), succeeded=True)

def PLAY(url):
    if xbmcplugin.getSetting(pluginhandle, "debug") == "true":
        xbmc.log("[PLUGIN :%s]\nPLAY(url):\nURL :%s" % (__addonname__, url))
    # Get current list item details...
    title = unicode(xbmc.getInfoLabel("ListItem.Title"), "utf-8")
    plot = unicode(xbmc.getInfoLabel("ListItem.Plot"), "utf-8")
    thumbnail = xbmc.getInfoImage("ListItem.Thumb")

    # Show wait dialog while parsing data...
    dialogWait = xbmcgui.DialogProgress()
    dialogWait.create(xbmc.getLocalizedString(30102), title)

    # Get video link...
    html = urllib.urlopen(url).read()
    video_url = re.findall("so.addVariable\('assetUrl', '(.+?)'\);", html)[0]

    # Debug
    if xbmcplugin.getSetting(pluginhandle, "debug") == "true":
        print "========================="
        print "VIDEO URL         = " + video_url
        print "========================="

    # Play video...
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()

    # only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
    listitem = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)

    # set the key information
    listitem.setInfo("Video", {"Title" : title,
                               "Label" : title,
                               "Plot" : plot})

    # add item to our playlist
    playlist.add(video_url, listitem)

    # Close wait dialog...
    dialogWait.close()
    del dialogWait

    # Play video...
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(playlist)

#------------------------------------------------------------------------------

def UpdateCheck(__version__, __addonname__):
    if xbmcplugin.getSetting(pluginhandle, "debug") == "true":
        xbmc.log("[PLUGIN :%s]\nUpdateCheck(__version__, __addonname__):" % __addonname__)
    import urllib2
    HEADER = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2'
    SVN_URL = 'http://code.google.com/p/queeup/source/browse/branches/plugins/video/%s/default.py'
    req = urllib2.Request(SVN_URL % __addonname__.replace(' ', '%20'))
    req.add_header('User-Agent', HEADER)
    f = urllib2.urlopen(req)
    a = f.read()
    f.close()
    ALL = re.compile('<td class="source">__version__ = &quot;(.+?)&quot;<br></td>').findall(a)
    for link in ALL :
        if link.find(__version__) != 0:
            newVersion = link
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(xbmc.getLocalizedString(30000),
                           xbmc.getLocalizedString(30103),
                           xbmc.getLocalizedString(30104) + __version__,
                           xbmc.getLocalizedString(30105) + newVersion)

#------------------------------------------------------------------------------

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
            params = sys.argv[2]
            cleanedparams = params.replace('?', '')
            if (params[len(params) - 1] == '/'):
                    params = params[0:len(params) - 2]
            pairsofparams = cleanedparams.split('&')
            param = {}
            for i in range(len(pairsofparams)):
                    splitparams = {}
                    splitparams = pairsofparams[i].split('=')
                    if (len(splitparams)) == 2:
                            param[splitparams[0]] = splitparams[1]
    return param

params = get_params()
mode = None
name = None
page = 1
url = None

try: mode = int(params['mode'])
except: pass
try: name = str(params['name'])
except: pass
try: page = int(params['page'])
except: pass
try: url = urllib.unquote_plus(params['url'])
except: pass

#------------------------------------------------------------------------------

if mode == None:
    #Update Check
    if xbmcplugin.getSetting(pluginhandle, "update") == "true":
        UpdateCheck(__version__, __addonname__)
    MAIN()
elif mode == 0: LIST(url, name, page)
elif mode == 1: PLAY(url)
