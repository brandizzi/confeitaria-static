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

from inelegant.fs import temp_file, temp_dir
from inelegant.finder import TestFinder

from confeitaria.static.store.file import FileStore

from confeitaria_static_tests.store.reference import ReferenceStoreTestCase


class TestFileStore(ReferenceStoreTestCase):

    def get_store(self, container):
        """
        Create a file store with the given arguments.
        """
        return FileStore(directory=container)

    def make_container(self):
        """
        Create a temporary directory to be given to the file store to be
        tested.
        """
        return temp_dir()

    def make_document(self, name, where, content='', path=None):
        """
        Create a temporary file to be given to the file store to be tested.
        """
        if path is not None:
            path = os.path.join(where, path)
            os.makedirs(path)
        else:
            path = where

        return temp_file(where=path, name=name, content=content)

    def test_raise_valueerror_if_outside_directory(self):
        """
        If the path leads to outside the directory given to the store, it
        it should raise ``ValueError``.
        """
        with temp_dir() as root_dir, \
                temp_dir(where=root_dir) as d, \
                temp_file(where=root_dir, name='passwd', content='mypass'):

            store = FileStore(directory=d)

            with self.assertRaises(ValueError):
                store.read('/../passwd')


load_tests = TestFinder(
    __name__,
    'confeitaria.static.store.file',
    skip=ReferenceStoreTestCase
).load_tests

if __name__ == '__main__':
    unittest.main()
