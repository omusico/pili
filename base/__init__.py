# -*- coding: utf-8 -*-
import re
import types
import inspect
import os

from pili import lite

class SimpleRoute(object):
    _methods = []

    def __init__(self, url_prefix):
        self.url_prefix = url_prefix.rstrip('/')
        # get function list
        self._methods = []
        for func in self.__class__.__dict__:
            if not re.match(r"[a-z]", func[0]) or type(self.__class__.__dict__[func]) is not types.FunctionType:
                continue
            if self.__class__.__name__ == getattr(self, func).im_class.__name__:
                self._methods.append(func)

    def run(self):
        if self.url_prefix + '/' == _ENV['PATH_INFO']:
            output = self._index()
        else:
            pattern = re.compile("%s/?\/(\w+)\/?(.*)" % re.escape(self.url_prefix))
            match = re.match(pattern, _ENV['PATH_INFO'])
            output = self._request(match.group(1), match.group(2))

        if output is not None:
            echo(output)

    def _index(self):
        pass

    def _default(self, *args):
        header('Status', '400 Bad Request')
        flush()

    def _error(self):
        header('Status', '400 Bad Request')
        flush()

    # /<controller>/ or /<controller>/<args>... go for this
    def _request(self, *args):
        action = '_default'
        if args[0] in self._methods:
            action = args[0]
        if args[0] + '_' in self._methods:
            action = args[0] + '_'
        if args[0] == '' and len(args) == 1:
            action = '_index'
            args = ()

        method = getattr(self, action)
        if action == '_default':
            output = self._default(args)
        elif len(args) > 1:
            output =  apply(method, args[1].split('/'))
        else:
            output = apply(method)

        if output is not None:
            echo(output)

lite.init(globals())
