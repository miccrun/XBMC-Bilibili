# coding: utf8
import gzip
from StringIO import StringIO
import tempfile
import urllib2
import xbmc
import zlib


def _get_gzip_content(content):
    return gzip.GzipFile(fileobj=StringIO(content), mode='rb').read()

def _get_zlib_content(content):
    return zlib.decompressobj(-zlib.MAX_WBITS).decompress(content)

def get_url_content(url):
    try:
        req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})
        response = urllib2.urlopen(req)
        print response.headers.get('content-encoding', '')
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
