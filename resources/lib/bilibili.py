#coding: utf8

from config import *
import xml.dom.minidom as minidom
import tempfile
import utils
from niconvert import create_website


def get_tmp_dir():
    if len(TEMP_DIR) != 0:
        return TEMP_DIR
    try:
        return tempfile.gettempdir()
    except:
        return TEMP_DIR


def print_info(info):
    print '[Bilibili]: ' + info


def get_video_urls(cid):
    interface_full_url = INTERFACE_URL.format(str(cid))
    print_info('Interface url: ' + interface_full_url)
    # 解析RSS页面
    print_info('Getting video address by interface page')
    content = utils.get_page_content(interface_full_url)
    print_info('Interface page length: ' + str(len(content)))
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
    page_full_url = COMMENT_URL.format(cid)
    print_info('Page full url: ' + page_full_url)
    website = None
    try:
        website = create_website(page_full_url)
        if website is None:
            print_info(page_full_url + " not supported")
            return ''
        else:
            print_info('Generating subtitle')
            text = website.ass_subtitles_text(
                font_name=u'黑体',
                font_size=56,
                resolution='%d:%d' % (WIDTH, HEIGHT),
                line_count=12,
                bottom_margin=0,
                tune_seconds=0
            )
            f = open(get_tmp_dir() + '/tmp.ass', 'w')
            f.write(text.encode('utf8'))
            f.close()
            print_info('Subtitle generation succeeded!')
            return 'tmp.ass'
    except Exception as e:
        print_info("Exception raised when generating subtitle: %s" % e)
        return ''
