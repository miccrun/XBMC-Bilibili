#coding: utf8
from xbmcswift2 import Plugin, xbmcgui, xbmc
from resources.lib.bilibili import *
from resources.lib.subtitle import subtitle_offset

plugin = Plugin()


def print_info(info):
    print '[BiliAddon]: ' + info


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
        time = float(self.getTime())
        if self.show_subtitle:
            print_info(self.subtitle)
            if time > 1:
                print_info('offset!')
                self.setSubtitles(subtitle_offset(self.subtitle, -time))
            else:
                print_info('no offset!')
                self.setSubtitles(self.subtitle)
        else:
            print_info('No subtitle')
            self.showSubtitles(False)


# 播放视频
@plugin.route('/video/<cid>/<show_comments>/')
def play_video(cid, show_comments):
    plugin.notify("Loading video...", "Bilibili", 1000)
    print_info('Getting video urls')
    video_list = get_video_urls(cid)
    count = len(video_list)
    print_info('%d videos found' % count)
    if count > 0:
        playlist = xbmc.PlayList(1)
        playlist.clear()
        list_item = xbmcgui.ListItem(u'Bilibili Video')
        list_item.setInfo(type='video', infoLabels={"Title": u"Bilibili Video"})

        stack_url = 'stack://' + ' , '.join(video_list)
        playlist.add(stack_url, list_item)
        player = BiliPlayer()
        player.play(playlist)
        if show_comments == '1':
            print_info('Play with subtitle')
            subtitle_path = get_subtitle(cid)
            print_info('subtitle path %s' % subtitle_path)
            player.setSubtitle(get_tmp_dir() + '/' + subtitle_path)
        else:
            print_info('Play without subtitle')
            player.showSubtitles(False)
            player.show_subtitle = False
        # while(not xbmc.abortRequested):
        xbmc.sleep(100)
    else:
        print_info('no video found')


if __name__ == '__main__':
    plugin.run()
