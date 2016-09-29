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


class StaticPage(confeitaria.interfaces.Page):
    """
    ``confeitaria.static.StaticPage`` is a Confeitaria page that serves content
    from static files.

    Its constructor receives the path of the directory containing the static
    files. If a requested file is found there, it will be served::

    >>> import requests
    >>> from inelegant.fs import temp_dir, temp_file
    >>> from confeitaria.server import Server
    >>> with temp_dir() as d,\\
    ...         temp_file(dir=d, name='index.html', content='example') as f:
    ...     page = StaticPage(directory=d)
    ...     with Server(page):
    ...         requests.get('http://localhost:8000/index.html').text
    ...         requests.get('http://localhost:8000/').text
    u'example'
    u'example'
    """

    def __init__(self, directory):
        self.directory = directory

    def index(self, *args):
        request = self.get_request()
        path = get_file_path(self.directory, request.args_path)

        try:
            with open(path) as f:
                content = f.read()
        except IOError:
            message = '"{0}" not found on this server.'.format(path)
            raise NotFound(message=message)

        return content


def get_file_path(root_dir, relative_path, index_file_name='index.html'):
    """
    Returns the path of a file inside a specific directory.

    Given a directory and a relative path, returns the first one joined with
    the relative path::

    >>> get_file_path('/a/b', 'c/d/file.txt')
    '/a/b/c/d/file.txt'

    If the relative path points to an existing directory, the returned path
    should have the name of a file appended to it (generally, ``index.html``)::

    >>> from inelegant.fs import temp_dir
    >>> with temp_dir() as d1, temp_dir(where=d1, name='d2'):
    ...     get_file_path(d1, 'd2').endswith('d2/index.html')
    True
    """
    path = os.path.join(root_dir, relative_path)

    if os.path.isdir(path):
        path = os.path.join(path, index_file_name)

    return path
