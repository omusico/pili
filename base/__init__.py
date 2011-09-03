# -*- coding: utf-8 -*-
from pili.ext import webapp2
import re
import types
import inspect
import os

class Base(webapp2.RequestHandler):
    _methods = []

    def __init__(self, request, response):
        self.initialize(request, response)

        # get function list
        self._methods = []
        for func in self.__class__.__dict__:
            if not re.match(r"[a-z]", func[0]) or type(self.__class__.__dict__[func]) is not types.FunctionType:
                continue
            if self.__class__.__name__ == getattr(self, func).im_class.__name__:
                self._methods.append(func)
        self._init()

    def _init(self):
        pass

    def _index(self):
        pass

    def _default(self, *args):
        self.response.set_status(400)

    def _error(self):
        self.response.set_status(400)

    # /<controller>/ or /<controller>/<args>... go for this
    def _request(self, *args):

        action = '_default'
        if args[0] in self._methods:
            action = args[0]
        if args[0] + '_' in self._methods:
            action = args[0] + '_'

        method = getattr(self, action)
        if action == '_default':
            output = self._default(args)
        elif len(args) > 1:
            output =  apply(method, args[1].split('/'))
        else:
            output = apply(method)

        if output is not None:
            self.response.write(output)

    def echo(self, text):
        self.response.write(text)


env = os.environ

route = webapp2.Route
create_app = webapp2.WSGIApplication

def create_simple_route(prefix, handler):
    return [
        route(prefix + '/<:[a-z]\w+>/', handler=handler, handler_method='_request'),
        route(prefix + '/<:[a-z]\w+>/<:.+>/', handler=handler, handler_method='_request'),
        route(prefix + '/', handler=handler, handler_method='_index'),
        route(prefix + '/<:.+>', handler=handler, handler_method='_default'),
        ]
        
    
