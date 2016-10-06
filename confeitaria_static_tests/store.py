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

import unittest

from inelegant.fs import temp_file, temp_dir
from inelegant.finder import TestFinder

from confeitaria.static.store import FileStore


class TestFileStore(unittest.TestCase):

    def test_read(self):
        """
        This tests ensures that ``FileStore`` can read the content of a file.
        """
        with temp_dir() as d, \
                temp_file(where=d, name='test.txt', content='read') as f:

            store = FileStore(directory=d)
            self.assertEquals('read', store.read('test.txt'))

    def test_read_default_file(self):
        """
        If given an empty path, the store should read content from a default
        file, if the file exists.
        """
        with temp_dir() as d, \
                temp_file(where=d, name='default.txt', content='default') as f:

            store = FileStore(directory=d, default_file_name='default.txt')
            self.assertEquals('default', store.read(''))

    def test_read_from_subdir(self):
        """
        The store should read content from files in a subdirectory.
        """
        with temp_dir() as d, \
                temp_dir(where=d, name='a/b/c') as sd, \
                temp_file(where=sd, name='sub.txt', content='subdir') as f:

            store = FileStore(directory=d)
            self.assertEquals('subdir', store.read('a/b/c/sub.txt'))

    def test_read_default_file_from_subdir(self):
        """
        If given a path to a dir, the store should read content from a default
        file, if the file exists.
        """
        with temp_dir() as d1, \
                temp_dir(where=d1, name='a/b/c') as d2, \
                temp_file(where=d2, name='test.txt', content='defsub') as f:

            store = FileStore(directory=d1, default_file_name='test.txt')
            self.assertEquals('defsub', store.read('a/b/c'))

    def test_raise_valueerror_on_not_found(self):
        """
        If the file does not exist, it should raise ``ValueError``.
        """
        with temp_dir() as d:
            store = FileStore(directory=d)

            with self.assertRaises(ValueError):
                store.read('nofile.txt')

    def test_raise_valueerror_on_not_found_on_subdir(self):
        """
        If the file does not exist on a subdirectory, it should raise
        ``ValueError``.
        """
        with temp_dir() as d1, \
                temp_dir(where=d1, name='a/b/c') as d2:

            store = FileStore(directory=d1)

            with self.assertRaises(ValueError):
                store.read('a/b/c/nofile.txt')

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

    def test_read_absolute_paths(self):
        """
        The store should resolve paths that are "absolute" - i.e., start with
        a slash.
        """
        with temp_dir() as d, \
                temp_dir(where=d, name='a/b/c') as sd, \
                temp_file(where=sd, name='sub.txt', content='subdir') as f:

            store = FileStore(directory=d)
            self.assertEquals('subdir', store.read('/a/b/c/sub.txt'))


load_tests = TestFinder(
    __name__,
    'confeitaria.static.store'
).load_tests

if __name__ == '__main__':
    unittest.main()
