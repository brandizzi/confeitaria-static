#!/usr/bin/env python
#
# Copyright 2015 Adam Victor Brandizzi
#
# This file is part of Confeitaria Static.
#
# Confeitaria Static is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Confeitaria Static is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Confeitaria Static.  If not, see <http://www.gnu.org/licenses/>.

import os

import confeitaria.interfaces
from confeitaria.responses import NotFound

from confeitaria.static.store.aggregate import AggregateStore
from confeitaria.static.store.file import FileStore
from confeitaria.static.store.resource import ResourceStore


class StaticPage(confeitaria.interfaces.Page):
    """
    ``confeitaria.static.StaticPage`` is a Confeitaria page that serves content
    from static files.

    Its constructor receives the path of the directory containing the static
    files. If a requested file is found there, it will be served::

    >>> import requests
    >>> from inelegant.fs import temp_dir, temp_file
    >>> from confeitaria.server import Server
    >>> from confeitaria.static.page import StaticPage
    >>> with temp_dir() as d,\\
    ...         temp_file(dir=d, name='index.html', content='example') as f:
    ...     page = StaticPage(directory=d)
    ...     with Server(page):
    ...         requests.get('http://localhost:8000/index.html').text
    ...         requests.get('http://localhost:8000/').text
    u'example'
    u'example'
    """

    def __init__(self, directory=None, store=None, resource_dir='content'):
        if store is None and directory is not None:
            primary = FileStore(directory=directory)
        else:
            primary = store

        secondary = ResourceStore(self.__module__, resource_dir)

        self.store = AggregateStore(primary, secondary)

    def index(self, *args):
        request = self.get_request()
        path = request.args_path

        try:
            content = self.store.read(path)
        except ValueError:
            raise NotFound(message='"{0}" not found.'.format(path))

        return content
