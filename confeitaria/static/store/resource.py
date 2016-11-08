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

    def __init__(self, package, default_file_name='index.html'):
        self.package = package
        self.default_file_name = default_file_name

    def read(self, path):
        try:
            return pkgutil.get_data(self.package, path)
        except IOError as e:
            if e.errno == errno.EISDIR:
                path = os.path.join(path, self.default_file_name)
                return self.read(path)
            else:
                raise ValueError('{0} not found.'.format(path))
