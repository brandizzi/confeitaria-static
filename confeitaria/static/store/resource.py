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

import pkgutil
import os.path
import errno


class ResourceStore(object):

    def __init__(self, package, directory, default_file_name='index.html'):
        """
        ``ResourceStore``` is a store to read content from package resources.

        Its constructor expects a package name and a directory inside this
        package. If there are resources inside this package directory, we can
        get the content of them by giving the ``read()`` method the resource
        path::

        >>> from inelegant.module import available_module, available_resource
        >>> with available_module('m'), \\
        ...         available_resource(
        ...             'm', 'test.html', where='resource_dir',
        ...             content='example'):
        ...     store = ResourceStore('m', 'resource_dir')
        ...     store.read('test.html')
        'example'

        If the resource does not exist, it will raise ``ValueError``::

        >>> with available_module('m'):
        ...     store = ResourceStore('m', 'resource_dir')
        ...     store.read('not_found.html')         # doctest: +ELLIPSIS
        Traceback (most recent call last):
          ...
        ValueError: ...
        """
        self.package = package
        self.directory = directory
        self.default_file_name = default_file_name

    def read(self, path):
        path = path.strip('/')
        resource_path = os.path.join(self.directory, path)

        try:
            return pkgutil.get_data(self.package, resource_path)
        except IOError as e:
            if e.errno == errno.EISDIR:
                resource_path = os.path.join(path, self.default_file_name)

                return self.read(resource_path)
            else:
                raise ValueError('{0} not found.'.format(path))
