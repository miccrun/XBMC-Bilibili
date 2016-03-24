# coding: utf-8

from config import *
from danmaku2ass.danmaku2ass import Danmaku2ASS
import tempfile
import utils
import xml.dom.minidom as minidom
import xbmc


def get_tmp_dir():
    if len(TEMP_DIR) != 0:
        return TEMP_DIR
    try:
        return tempfile.gettempdir()
    except:
        return TEMP_DIR


def print_info(info):
    xbmc.log("[BiliAddon] %s" % info, level=xbmc.LOGERROR)


def get_video_urls(cid):
    interface_full_url = INTERFACE_URL.format(str(cid))
    print_info('Interface url: ' + interface_full_url)
    # 解析RSS页面
    content = utils.get_page_content(interface_full_url)
    doc = minidom.parseString(content)
    parts = doc.getElementsByTagName('durl')
    print_info('Video parts found: ' + str(len(parts)))
    result = []
    # 找出所有视频地址
    for part in parts:
        urls = part.getElementsByTagName('url')
        if len(urls) > 0:
            result.append(urls[0].firstChild.nodeValue)
    return result


def get_subtitle(cid):
    url = COMMENT_URL.format(cid)
    print_info('Page full url: ' + url)
    input = get_tmp_dir() + '/tmp.xml'
    output = get_tmp_dir() + '/tmp.ass'

    local_file = open(input, "w")
    local_file.write(utils.get_page_content(url))
    local_file.close()

    Danmaku2ASS(input, output, WIDTH, HEIGHT,
        font_size=FONT_SIZE,
        text_opacity=TEXT_OPACITY,
        is_reduce_comments=IS_REDUCE_COMMENTS,
        duration_marquee=DURATION_MARQUEE,
        duration_still=DURATION_STILL
    )
    return output
