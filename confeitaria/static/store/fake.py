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


class FakeStore(object):


    def __init__(self, documents, default_file_name='index.html'):
        self.documents = documents
        self.default_file_name = default_file_name

    def read(self, path):
        default_path = os.path.join(path, self.default_file_name)

        if path not in self.documents and default_path in self.documents:
            path = default_path

        path = path.lstrip('/')

        try:
            content = self.documents[path]
        except Exception as e:
            raise ValueError(
                'Failed to read {0}. Reason: {1}'.format(path, e))

        return content
