# coding: utf-8
import time
import xbmc, xbmcgui
from xbmcswift2 import Plugin
from resources.lib.utils import print_info
from resources.lib.bilibili import get_video


class BiliPlayer(xbmc.Player):
    def __init__(self):
        self.position = []

    def setSubtitlePosition(self, position):
        self.position = position

    def onPlayBackStarted(self):
        print_info('On playback started, set subtitle')
        time = int(self.getTime())
        for index, value in enumerate(self.position):
            if time >= value[0] and time < value[1]:
                subtitle_path = '/tmp/' + str(index + 1) + '.ass'
                self.setSubtitles(subtitle_path)
                self.showSubtitles(True)
                print_info('Setting subtitle: ' + subtitle_path)
                break


print_info('Init add-on')
player = BiliPlayer()
plugin = Plugin()
start_timestamp = str(int(time.time()))


@plugin.route('/video/<av>/<page>')
def play_video(av, page):
    xbmcgui.Window(10000).setProperty("StartTimestamp", start_timestamp)
    plugin.notify("Loading video...", "Bilibili", 1000)

    result = get_video(av, page)
    count = len(result['videos'])
    if count > 0:
        playlist = xbmc.PlayList(1)
        playlist.clear()
        list_item = xbmcgui.ListItem(u'Bilibili Video')
        list_item.setInfo(type='video', infoLabels={"Title": u"Bilibili Video"})

        stack_url = 'stack://' + ' , '.join(result['videos'])
        playlist.add(stack_url, list_item)
        player.setSubtitlePosition(result['position'])
        player.play(playlist)
    else:
        plugin.notify("No Video Found", "Bilibili", 100)


if __name__ == '__main__':
    plugin.run()


monitor = xbmc.Monitor()
while not monitor.abortRequested():
    # Sleep/wait for abort for 1 seconds
    if monitor.waitForAbort(1):
        # Abort was requested while waiting. We should exit
        break
    if xbmc.getInfoLabel("Window(10000).Property(StartTimestamp)") != start_timestamp:
        print_info('New video played, add-on ends here')
        break
