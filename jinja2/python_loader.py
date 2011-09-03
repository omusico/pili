# -*- coding: utf-8 -*-

import logging
from jinja2.loaders import FileSystemLoader
from google.appengine.api import memcache
import os
import hashlib

try:
    mydata
except NameError:
    #logging.error("damn")
    mydata = {}

import base64
def get_data_by_name(name):
    if base64.b64encode(name) in mydata:
        return mydata[base64.b64encode(name)]
    return None

def tpl_min(tpl, types=['jinja_comment','html_comment', 'blank_start']):
    import re
    if 'jinja_comment' in types:
        pattern = re.compile("\{#.*?#\}", re.I|re.M|re.S)
        tpl = re.sub(pattern, r"", tpl)
    if 'html_comment' in types:
        pattern = re.compile("<!\-\-.*?\-\->", re.I)
        tpl = re.sub(pattern, r"", tpl)
    if 'blank_start' in types:
        pattern = re.compile("^\s+",re.M)
        tpl = re.sub(pattern, "", tpl)
    return tpl

class PythonLoader(FileSystemLoader):
    """A Jinja2 loader that loads pre-compiled templates."""
    def load(self, environment, name, globals=None):
        """Loads a Python code template."""
        if globals is None:
            globals = {}

        prefix = "::".join(self.searchpath)
        if os.path.dirname(__file__).find("/base/data/home") > -1:
            prefix += os.path.dirname(__file__)
            cache = True
            debug = False
        else:
            cache = False
            debug = True

        m = hashlib.md5()
        m.update(prefix)
        prefix = m.hexdigest()

        #try for a variable cache
        code = get_data_by_name(prefix + name)
        if cache and code is not None:
            if debug:
                logging.info("ultrafast memcache")
        else:
            if debug:
                logging.info("slow memcache")
            code = memcache.get(prefix+name)
            if not cache or code is None:
                if debug:
                    logging.info("oops no memcache!!")
                source, filename, uptodate = self.get_source(environment, name)
                template = file(filename).read().decode('utf-8') #.decode('ascii').decode('utf-8')
                template = tpl_min(template)
                code = environment.compile(template, raw=True)
                memcache.set(prefix+name, code)
                if debug:
                    logging.info(prefix+name)
            else:
                if debug:
                    logging.info("yeh memcache")
            code = compile(code, name, 'exec')
            mydata[base64.b64encode(prefix+name)] = code
        return environment.template_class.from_code(environment, code, globals)

