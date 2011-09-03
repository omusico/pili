from jinja2 import Environment,FileSystemLoader
from python_loader import PythonLoader
import jinjafilter

from google.appengine.api import memcache
import os
from types import DictType
import hashlib
import logging

try:
    _pre_cache
except NameError:
    _pre_cache = dict()

"""
tpl = jinja2.create_jinja("../../tpls")
tpl.assign({"name":"pili engine"})
self.response.write(tpl.render("index.html"))

default cache_time is 1 day
"""
class create_jinja:

    cache_time = 86400

    def __init__(self, *a, **kwargs):
        self.clear_all_assign()
        self.cache_time = 86400

        # add current file path in to prefix key, 
        #it's able to include each updates for Google App Engine
        self._cache_key_prefix = os.path.dirname(__file__) + "::" + str(a)
        extensions = kwargs.pop('extensions', [])
        globals = kwargs.pop('globals', {})

        self._lookup = Environment(loader=PythonLoader(*a, **kwargs), extensions=extensions)
        self._lookup.globals.update(globals)

        #now is not available to use byteccode cache
        #from jinja2.bccache import MemcachedBytecodeCache
        #from google.appengine.api import memcache
        #self._render._lookup.bytecode_cache = MemcachedBytecodeCache(memcache, self.config.CACHE_KEY_PREFIX)

        #add useful filters
        self._lookup.filters.update({'urlencode':jinjafilter.__dict__['urlencode']})

    # add filter/modifier
    # tpl.add_filter({'urlencode':urlencode_func})
    def add_filter(filters):
        self._lookup.filters.update(filters)

    def clear_all_assign(self):
        self._data = {}

    # tpl.assign({"name":"pili"})
    # tpl.assign("name", "pili")
    def assign(self, *args):
        if len(args) == 1:
            self._data.update(args[0])
        elif len(args) == 2:
            self._data[args[0]] = args[1]

    # cache cached from memcache
    # since memcache is not able to check cached or not
    # this function is going to get the result from memcache
    # it cached the result in memory and then make render() to get result faster
    def is_cached(self, tpl, cache_key=''):
        key = cache_key + tpl
        rst = memcache.get(key, self._cache_key_prefix)
        if rst is None:
            return False
        else:
            # cache the result into memory first
            key2 = hashlib.md5(key + self._cache_key_prefix).hexdigest()
            _pre_cache = dict()
            _pre_cache[key2] = rst
            return True

    # once cache_time set, cache will be enable
    # template directory and template file construct a cache key by default
    # you appened extra cache_key to determine different data
    # parameter could be (tpl, data) or (tpl, cache_key='', cache_time =86400)
    # note: data param cannot be passed if you want to use cache
    def render(self, tpl, *args, **kwargs): #data=None, cache_time=None, cache_key=''):

        # data param
        data = None
        if len(args) == 1 and type(args[0]) is DictType:
            data = args[0]
        elif 'data' in kwargs:
            data = kwargs.pop('data')

        if data is not None:
            self.assign(kwargs.pop('data'))
            return self._lookup.get_template(tpl).render(self._data)

        # only have cache params
        if data is None:
            cache = False
            if len(args)>=1:
                cache = True
                if len(args) == 1:
                    cache_key = args[0]
                    cache_time = self.cache_time
                elif len(args) == 2:
                    cache_key, cache_time = args
            elif len(kwargs)>=1:
                cache = True
                cache_key = kwargs.get('cache_key', '')
                cache_time = kwargs.get('cache_time', self.cache_time)

        if cache:
            key = cache_key + tpl
            key2 = hashlib.md5(key + self._cache_key_prefix).hexdigest()
            if key2 in _pre_cache:
                rst = _pre_cache[key2]
            else:
                rst = memcache.get(key, self._cache_key_prefix)
            if rst is None:
                rst = self._lookup.get_template(tpl).render(self._data)
                memcache.set(key, rst, time = cache_time, namespace = self._cache_key_prefix)
            return rst
        else:
            return self._lookup.get_template(tpl).render(self._data)

