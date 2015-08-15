# coding: utf8
import gzip
from StringIO import StringIO
import urllib2
import zlib


def _get_gzip_content(content):
    return gzip.GzipFile(fileobj=StringIO(content), mode='rb').read()


def _get_zlib_content(content):
    return zlib.decompressobj(-zlib.MAX_WBITS).decompress(content)


def get_page_content(page_full_url):
    try:
        req = urllib2.Request(page_full_url, headers={'User-Agent': 'Mozilla/5.00 (Macintosh; Intel Mac OS X 10.110; rv:40.00) Gecko/20100101 Firefox/40.00'})
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
