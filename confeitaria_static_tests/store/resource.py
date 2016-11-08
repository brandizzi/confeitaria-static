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
import os.path

import unittest

from inelegant.module import available_module, available_resource
from inelegant.fs import temp_file, temp_dir
from inelegant.finder import TestFinder

from confeitaria.static.store.resource import ResourceStore

from confeitaria_static_tests.store.reference import ReferenceStoreTestCase


class ReferenceTestResourceStore(ReferenceStoreTestCase):

    def get_store(self, container, default_file_name=None):
        """
        Create a resource store with the given arguments.
        """
        return ResourceStore('m', default_file_name=default_file_name)

    def make_container(self):
        """
        Create an available module to add resources to.
        """
        return available_module('m')

    def make_document(self, name, where, content='', path=None):
        """
        Create a temporary resource in the "m" package.
        """
        if path is not None:
            name = os.path.join(path, name)

        return available_resource('m', name, content=content)


load_tests = TestFinder(
    __name__,
    'confeitaria.static.store.file',
    skip=ReferenceStoreTestCase
).load_tests

if __name__ == '__main__':
    unittest.main()
