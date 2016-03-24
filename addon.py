# coding: utf-8

from xbmcswift2 import Plugin
import xbmc, xbmcgui
import time
from resources.lib.bilibili import *
from resources.lib.subtitle import subtitle_offset

plugin = Plugin()

def print_info(info):
    xbmc.log("[BiliAddon] %s" % info, level=xbmc.LOGERROR)


class BiliPlayer(xbmc.Player):
    def __init__(self):
        self.subtitle = ""
        self.show_subtitle = False

    def setSubtitle(self, subtitle):
        if len(subtitle) > 0:
            self.show_subtitle = True
        else:
            self.show_subtitle = False
        self.subtitle = subtitle

    def onPlayBackStarted(self):
        print_info('on playback started, set subtitle')
        time = float(self.getTime())
        if self.show_subtitle:
            print_info(self.subtitle)
            if time > 1:
                print_info('offset! %d' % time)
                self.setSubtitles(subtitle_offset(self.subtitle, -time))
            else:
                print_info('no offset!')
                self.setSubtitles(self.subtitle)
        else:
            self.showSubtitles(False)

print_info('init player')
player = BiliPlayer()
start_timestamp = str(int(time.time()))

# 播放视频
@plugin.route('/video/<cid>/<show_comments>/')
def play_video(cid, show_comments):
    xbmcgui.Window(10000).setProperty("StartTimestamp", start_timestamp)
    plugin.notify("Loading video...", "Bilibili", 1000)
    print_info('Getting video urls')
    video_list = get_video_urls(cid)
    count = len(video_list)
    if count > 0:
        playlist = xbmc.PlayList(1)
        playlist.clear()
        list_item = xbmcgui.ListItem(u'Bilibili Video')
        list_item.setInfo(type='video', infoLabels={"Title": u"Bilibili Video"})

        stack_url = 'stack://' + ' , '.join(video_list)
        playlist.add(stack_url, list_item)
        if show_comments == '1':
            print_info('Play with subtitle')
            subtitle_path = get_subtitle(cid)
            print_info('subtitle path %s' % subtitle_path)
            player.setSubtitle(subtitle_path)
        else:
            print_info('Play without subtitle')
            player.showSubtitles(False)
            player.show_subtitle = False
        player.play(playlist)
    else:
        print_info('no video found')

    print_info('play route end')


if __name__ == '__main__':
    plugin.run()

monitor = xbmc.Monitor()
while not monitor.abortRequested():
    # Sleep/wait for abort for 1 seconds
    if monitor.waitForAbort(1):
        # Abort was requested while waiting. We should exit
        break
    if xbmc.getInfoLabel("Window(10000).Property(StartTimestamp)") != start_timestamp:
        print_info('new video played, add-on ends here')
        break
