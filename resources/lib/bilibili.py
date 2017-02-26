# coding: utf-8
import json
import re
import config
from danmaku2ass.danmaku2ass import Danmaku2ASS
import utils
from utils import print_info


def get_video(av, page):
    interface_url = config.INTERFACE_URL.format(str(av), str(page))
    print_info('Interface url: ' + interface_url)
    data = utils.get_url_content(interface_url)
    json_obj = json.loads(data)

    last_time = 0
    result = {}
    result['videos'] = []
    result['position'] = []
    cid = json_obj['cid']
    for value in json_obj['data']:
        if value['name'] == u"\u8d85\u6e05FLV":
            for item in value['parts']:
                res = re.search('^(\d{2}):(\d{2})', item['length'])
                video_length = int(res.group(1)) * 60 + int(res.group(2))
                result['position'].append((last_time, last_time + video_length))
                result['videos'].append(item['url'])
                last_time += video_length
    get_subtitle(cid)

    return result

def get_subtitle(cid):
    url = config.COMMENT_URL.format(str(cid))
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
