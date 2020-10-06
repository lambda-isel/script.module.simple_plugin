# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2020-present lambda-isel (https://github.com/lambda-isel)

from sys import argv
from urlparse import parse_qsl
from urllib import urlencode
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItems, endOfDirectory, setContent


class SimplePlugin(object):

    def __init__(self):
      self.url = argv[0]
      self.handle = int(argv[1])
      self.method = 'method'

    def add(self, items=[], success=True, update=False, cache=True):
        addDirectoryItems(self.handle, items, len(items))
        endOfDirectory(self.handle, success, update, cache)

    def listitem(self, url, label='', label2='', art=None, info=None, properties=None, is_folder=True):
        listitem = ListItem(label, label2)
        if art:
            listitem.setArt(art)
        if info:
            listitem.setInfo(*info)
        if properties:
            listitem.setProperties(properties)
        return (url, listitem, is_folder)

    def route(self):
        args = {l[0]: l[1] for l in parse_qsl(argv[2][1:])}
        return getattr(self, args.pop(self.method, 'root'))(**args)

    def run(self):
        self.add([self.listitem(**item) for item in self.route()])

    def set_content(self, content):
        setContent(self.handle, content)

    def url_for(self, method, **kwargs):
        kwargs[self.method] = method.__name__
        return '{}?{}'.format(self.url, urlencode(kwargs))

    def root(self):
        return []
