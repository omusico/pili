#!/usr/bin/env python
import sys
import types
import os
import urllib
import cgi
import logging
from Cookie import SimpleCookie

# instance
_liter = None

def init(g, refresh=None):
    _liter.init(g, refresh)

class Lite:
    request = None
    def __init__(self):
        pass

    def init(self, g, refresh = None):

        if refresh is True or refresh is None and g.get('__name__') == '__main__':
            self._init_vars()

        g2 = globals()

        # setup functions
        for name in ('echo', 'header', 'setcookie','ob_start','ob_get_clean','flush'):
            if name not in g:
                g[name] = g2['_' + name]

        # setup instance or variable
        for name in ('ENV', 'GET', 'GETS', 'POST', 'POSTS', 'COOKIE', 'FILE'):
            g['_' + name] = g2['_'+name]

    def _init_vars(self):
        # setup variables
        global _content, _headers, _cookies, _ENV, _GET,_GETS, _POST,_POSTS, \
            _COOKIE, _FILE, _ob, _headers_sent
        _headers_sent = False
        _ob = False
        _content = ''
        _headers = {"Content-Type":'text/html; charset=utf-8'}
        _cookies = dict()

        _ENV = ENV()
        _GET = GET()
        _GETS = GETS()
        _POST = POST()
        _POSTS = POSTS()
        _COOKIE = COOKIE()
        _FILE = FILE()


def ENV():
    return os.environ

class _INPUT:
    _cache = {}
    def __init__(self):
        self._cache = dict()

    def __call__(self, name, default=None):
        rst = self.__getitem__(name)
        if rst is None:
            return default
        return rst

    def _urldecode(self, txt):
        return urllib.unquote_plus(txt)

class GET(_INPUT):
    def __getitem__(self, key):
        return self._get(key)

    def _get(self, key, multiple=False):
        cache_key = str(multiple) + key
        if cache_key in self._cache:
            return self._cache[cache_key]

        global _ENV
        gets = _ENV['QUERY_STRING'].split("&")
        rst = list()
        for get in gets:
            if get.find("=")<1:
                continue
            k, v = get.split("=", 1)
            if k==key:
                if multiple:
                    rst.append(self._urldecode(v))
                else:
                    self._cache[cache_key] = self._urldecode(v)
                    return self._urldecode(v)
        if multiple:
            self._cache[cache_key] = rst
            return rst
        self._cache[cache_key] = None

class GETS(GET):
    def __getitem__(self, key):
        return self._get(key, True)

class POST(_INPUT):
    def __getitem__(self, key):
        return self._post(key)

    def _post(self, key, multiple=False):
        cache_key = str(multiple) + key
        if cache_key in self._cache:
            return self._cache[cache_key]

        form = cgi.FieldStorage()
        if multiple:
            self._cache[cache_key] = form.getlist(key)
        else:
            self._cache[cache_key] = form.getfirst(key, None)
        return self._cache[cache_key]

class POSTS(POST):
    def __getitem__(self, key):
        return self._post(key, True)

"""Get uploaded File
<form enctype="multipart/form-data" ... >
    <input type="file" name="somename">
</form>

header("Content-Type: image/png")
flush() # output header
print _FILE['somename'].file.read()
"""
class FILE():
    def __getitem__(self, key):
        form = cgi.FieldStorage()
        return form[key]

class COOKIE(_INPUT):
    def __getitem__(self, name):
        if name in self._cache:
            return self._cache[name]
        else:
            self._cache[name] = None            
        global _ENV
        C = SimpleCookie()
        C.load(_ENV['HTTP_COOKIE'])
        if name in C:
            self._cache[name] = self._urldecode(C[name].value)
        return self._cache[name]

def _setcookie(name, value, **kwargs):
    global _cookies

    httponly = False
    if float('.'.join(sys.version.split('.', 3)[:2]))<2.6 and \
        'httponly' in kwargs:
        httponly = kwargs.pop('httponly')

    C = SimpleCookie()
    C[name] = urllib.quote_plus(value)
    for key in kwargs:
        C[name][key.replace('_','-')] = kwargs[key]
    _cookies[name] = C.output()
    
    if httponly:
        _cookies[name] += '; HttpOnly'
    _header("\n".join([ _cookies[k] for k in _cookies]))

def _header(*args):
    global _headers_sent, _headers
    if _headers_sent is True:
        logging.error("header already sent")
        return
    if len(args) == 1:
        k,v = args[0].split(":", 1)
        _headers[k] = v.lstrip()
    else:
        _headers[args[0]]  = args[1]

def _ob_start():
    global _ob
    _ob = True

def _ob_get_clean():
    global _ob, _content
    _ob = False
    c = _content + ""
    _content = ""
    return c

def _echo(*args):
    global _headers_sent, _ob, _content

    if _ob is False and _headers_sent is False:
        _headers_sent = True
        for k,v in _headers.iteritems():
            print "%s: %s" % (k,v)
        print ""

    for txt in args:
        if _ob is True:
            if type(txt) is types.UnicodeType:
                _content += txt.encode('utf-8')
            else:
                _content += str(txt)
        else:
            if type(txt) is types.StringType:
                sys.stdout.write(txt)
            elif type(txt) is types.UnicodeType:
                sys.stdout.write(txt.encode('utf-8'))
            else:
                sys.stdout.write(str(txt))

def _flush():
    _echo(_ob_get_clean())

_liter = Lite()

