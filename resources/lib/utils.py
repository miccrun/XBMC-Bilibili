# coding: utf8
import gzip
from StringIO import StringIO
import urllib2
import zlib
import tempfile


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
    if len(TEMP_DIR) != 0:
        return TEMP_DIR
    try:
        return tempfile.gettempdir()
    except:
        return TEMP_DIR
