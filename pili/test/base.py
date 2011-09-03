# -*- coding: utf-8 -*-
from pili import base
from pili import jinja2
from pili.ext import webapp2

import os
import time

class WebApp(base.Base):
    def _init(self):
        pass

    def _index(self):
        self.response.write('this is index')

    def test(self,*args):
        self.response.write('this is test')

    # conflict name
    def echo_(self, *args):
        self.echo(args)
"""
    def cache(self):
        if self.tpl.is_cached('index.html') is False:
            self.tpl.assign('data', str(time.time()))
        self.echo(self.tpl.render('index.html', '', 5))
    
    def cache2(self):
        if self.tpl.is_cached('index.html') is False:
            self.tpl.assign({'data':str(time.time())})
        self.echo(self.tpl.render('index.html', cache_time=5))
"""

app = webapp2.WSGIApplication(base.create_simple_route('/_pili/test/base', WebApp))

def main():
    app.run()

if __name__ == "__main__":
    main()

