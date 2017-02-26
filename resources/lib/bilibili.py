# coding: utf-8
from danmaku2ass.danmaku2ass import Danmaku2ASS
import config
import utils
import xbmc
import json


def print_info(info):
    xbmc.log("[BiliAddon] %s" % info, level=xbmc.LOGERROR)


def get_video_urls(av, page):
    interface_full_url = config.INTERFACE_URL.format(str(av), str(page))
    print_info('Interface url: ' + interface_full_url)
    data = utils.get_url_content(interface_full_url)
    json_obj = json.loads(data)

    result = []
    for value in json_obj['data']:
        if value['name'] == u"\u8d85\u6e05FLV":
            for item in value['parts']:
                result.append(item['url'])

    return result

def get_subtitle(cid):
    url = config.COMMENT_URL.format(cid)
    print_info('Comment url: ' + url)
    input = utils.get_tmp_dir() + '/tmp.xml'
    output = utils.get_tmp_dir() + '/tmp.ass'

    local_file = open(input, "w")
    local_file.write(utils.get_url_content(url))
    local_file.close()

    Danmaku2ASS(input, output, config.WIDTH, config.HEIGHT,
        font_size=config.FONT_SIZE,
        text_opacity=config.TEXT_OPACITY,
        is_reduce_comments=config.IS_REDUCE_COMMENTS,
        duration_marquee=config.DURATION_MARQUEE,
        duration_still=config.DURATION_STILL
    )
    return output
