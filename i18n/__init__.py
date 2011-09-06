# -*- coding: utf-8 -*-

class I18n():
    def __init__(self, lang='en-US', path='i18n', type_='file'):
        self.lang = lang
        self.path = path
        self.type_ = type_

    def get(self, key):
        if self.type_ == 'file':
            return self._get_file(key)

    def _get_file(self, key):
        key = key.replace('/', '.')
        if '.' in key:
            module, obj = key.rsplit('.', 1)
            module = self.path + '.' + module + '.' + self.lang.replace('-','_')
            return getattr(__import__(module, None, None, [obj]), obj).decode('utf-8')

