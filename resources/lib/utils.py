# coding: utf8
import datetime
import gzip
from StringIO import StringIO
import tempfile
import urllib2
import xbmc
import zlib


TIME_FORMAT = '{0:d}:{1:02d}:{2:02d}.{3:02d}'

def _get_gzip_content(content):
    return gzip.GzipFile(fileobj=StringIO(content), mode='rb').read()

def _get_zlib_content(content):
    return zlib.decompressobj(-zlib.MAX_WBITS).decompress(content)

def get_url_content(url):
    try:
        req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})
        response = urllib2.urlopen(req)
        if response.headers.get('content-encoding', '') == 'gzip':
            return _get_gzip_content(response.read())
        elif response.headers.get('content-encoding', '') == 'deflate':
            return _get_zlib_content(response.read())
        else:
            return response.read()
    except Exception as e:
        print e
        return ''

def get_tmp_dir():
    try:
        return tempfile.gettempdir()
    except:
        return '/tmp'

def print_info(info):
    xbmc.log("[BiliAddon] %s" % info, level=xbmc.LOGERROR)


def _parse_time(time_str):
    time_split = time_str.split(':')
    hour = int(time_split[0])
    minute = int(time_split[1])
    second_and_microsecond = time_split[2].split('.')
    second = int(second_and_microsecond[0])
    microsecond = int(second_and_microsecond[1])
    origin_time = datetime.datetime(1000, 1, 2, hour, minute, second, microsecond)
    return origin_time

def subtitle_offset(input, output, start_offset, end_offset):
    start_offset = int(round(start_offset))
    end_offset = int(round(end_offset))
    subtitle_file = open(input)
    target_subtitle_file = open(output, 'w')
    is_events_line = False
    is_title_line = True

    for line in subtitle_file:
        if is_title_line and not is_events_line and '[Events]' in line:
            is_events_line = True
            target_subtitle_file.write(line)
            continue
        if is_title_line and is_events_line:
            is_title_line = False
            target_subtitle_file.write(line)
            continue

        if is_events_line:
            elements = line.split(',')
            time_delta = datetime.timedelta(seconds=-start_offset)
            video_start_time = datetime.datetime(1000, 1, 2, 0, 0, 0, 0)
            video_end_time = video_start_time + datetime.timedelta(seconds=(end_offset-start_offset))

            start_time = _parse_time(elements[1])
            end_time = _parse_time(elements[2])
            start_time += time_delta
            end_time += time_delta

            if start_time < video_start_time:
                continue
            elif start_time > video_end_time:
                continue
            else:
                start_time = start_time.time()
                end_time = end_time.time()
                elements[1] = TIME_FORMAT.format(start_time.hour, start_time.minute, start_time.second, start_time.microsecond)
                elements[2] = TIME_FORMAT.format(end_time.hour, end_time.minute, end_time.second, end_time.microsecond)
                target_line = ','.join(elements)
                target_subtitle_file.write(target_line)
        else:
            target_subtitle_file.write(line)
    subtitle_file.close()
    target_subtitle_file.close()
