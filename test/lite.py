#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "/home/girvan/google_appengine")
import dev_appserver
dev_appserver.fix_sys_path()

import unittest
from google.appengine.api import urlfetch

class liteTest(unittest.TestCase):
    _url_prefix = 'http://localhost/_pili/test'

    def setUp(self):
        pass

    def testEcho(self):
        url =  self._url_prefix + "/case-lite-basic/"
        result = urlfetch.fetch(url)
        print ""
        print result
        pass
    pass

if __name__=="__main__":
    print ""
    import logging

    logging.info("\n"*10)
    unittest.main()
    #unittest.main(defaultTest='ViewTest')

