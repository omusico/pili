# -*- coding: utf-8 -*-
import logging

class I18n():
    def __init__(self, lang='en-US', path='i18n', type_='file', default_lang='en-US'):
        self.lang = lang
        self.path = path
        self.type_ = type_
        self.default_lang = default_lang

    def get(self, key):
        if self.type_ == 'file':
            result = self._get_file(key)
            if not result and self.lang!=self.default_lang:
                logging.info("[i18n] %s fall back to %s from %s" % (key, self.default_lang, self.lang))
                result = self._get_file(key, self.default_lang)
            return result


    def _get_file(self, key, lang=None):
        if lang == None:
            lang = self.lang
        key = key.replace('/', '.')
        if '.' in key:
            module, obj = key.rsplit('.', 1)
            module = self.path + '.' + module + '.' + lang.replace('-','_')
            try:
                return getattr(__import__(module, None, None, [obj]), obj).decode('utf-8')
            except:
                logging.info("[i18n] Cannot get %s in %s" % (key,lang))
                return ""

