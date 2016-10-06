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


class FileStore(object):
    """
    ``FileStore`` is the object responsible to access a file given an path. To
    be created, it needs to know the directory where to find the file::

    >>> from inelegant.fs import temp_dir, temp_file
    ... with temp_dir() as d:
    ...     store = FileStore(directory=d)

    If the directory exists, it will read content of the files in it with the
    ``read()`` command::

    >>> with temp_dir() as d, \\
    ...         temp_file(where=d, name='test.html', content='example'):
    ...     store = FileStore(directory=d)
    ...     store.read('test.html')
    'example'

    If the path is a directory, it will try to read ``index.html`` in it by
    default::

    >>> with temp_dir() as d, \\
    ...         temp_file(where=d, name='index.html', content='default'):
    ...     store = FileStore(directory=d)
    ...     store.read('')
    'default'

    If no file exists, the ``read()`` method raises ``ValueError``::

    >>> with temp_dir() as d:
    ...     store = FileStore(directory=d)
    ...     store.read('nofile.html')   # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    ValueError: ...
    """

    def __init__(self, directory, default_file_name='index.html'):
        self.directory = directory
        self.default_file_name = default_file_name

    def read(self, path):
        path = get_file_path(
            self.directory, path, default_file_name=self.default_file_name)

        try:
            if not is_parent(self.directory, path):
                raise ValueError(
                    '{0} is not in {1}'.format(path, self.directory))

            with open(path) as f:
                content = f.read()
        except IOError as e:
            raise ValueError(
                'Failed to read {0}. Reason: {1}'.format(path, e))

        return content


def get_file_path(root_dir, relative_path, default_file_name='index.html'):
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
    ...     os.path.basename(get_file_path(d1, 'd2'))
    'index.html'

    The default file name can be overriden::

    >>> from inelegant.fs import temp_dir
    >>> with temp_dir() as d1, temp_dir(where=d1, name='d2'):
    ...     path = get_file_path(d1, 'd2', default_file_name='test.txt')
    ...     os.path.basename(path)
    'test.txt'
    """
    relative_path = relative_path.lstrip('/')

    path = os.path.join(root_dir, relative_path)

    if os.path.isdir(path):
        path = os.path.join(path, default_file_name)

    return path


def is_parent(parent_path, path):
    """
    ``is_parent()`` checks if ``path`` is inside ``parent_path``. If it is,
    ``is_parent()`` returns ``True``::

    >>> is_parent('/a/b/', '/a/b/c')
    True
    >>> is_parent('/a/b', '/a/b')
    True
    >>> is_parent('/a/b', '/a/c')
    False
    >>> is_parent('/a/b', '/a/b/../c')
    False
    """
    parent_path = os.path.realpath(parent_path)
    path = os.path.realpath(path)

    if parent_path == path:
        value = True
    elif is_root(path):
        value = False
    else:
        value = is_parent(parent_path, os.path.dirname(path))

    return value


def is_root(path):
    """
    ``is_root()`` checks if ``path`` is the root directory::

    >>> is_root(os.path.abspath(os.sep))
    True
    >>> is_root('/a/b')
    False
    """
    return os.path.dirname(path) == path
