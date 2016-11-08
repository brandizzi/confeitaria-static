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

from inelegant.fs import temp_file, temp_dir
from inelegant.finder import TestFinder


class ReferenceStoreTestCase(unittest.TestCase):

    def test_read(self):
        """
        This tests ensures that the store can read the content of a file.
        """
        with self.make_container() as d, \
                self.make_document('test.txt', where=d, content='read') as f:

            store = self.get_store(container=d)
            self.assertEquals('read', store.read('test.txt'))

    def test_read_default_file(self):
        """
        If given an empty path, the store should read content from a default
        file, if the file exists.
        """
        with self.make_container() as d, \
                self.make_document('default.txt', where=d, content='abc') as f:

            store = self.get_store(
                container=d, default_file_name='default.txt')
            self.assertEquals('abc', store.read(''))

    def test_read_from_subdir(self):
        """
        The store should read content from files in a subdirectory.
        """
        with self.make_container() as d, \
                self.make_document(
                    'sub.txt', where=d, path='a/b/c', content='subdir') as f:

            store = self.get_store(container=d)
            self.assertEquals('subdir', store.read('a/b/c/sub.txt'))

    def test_read_default_file_from_subdir(self):
        """
        If given a path to a dir, the store should read content from a default
        file, if the file exists.
        """
        with self.make_container() as d, \
                self.make_document(
                    'test.txt', where=d, path='a/b/c', content='defsub') as f:

            store = self.get_store(container=d, default_file_name='test.txt')
            self.assertEquals('defsub', store.read('a/b/c'))

    def test_raise_valueerror_on_not_found(self):
        """
        If the file does not exist, it should raise ``ValueError``.
        """
        with self.make_container() as d:
            store = self.get_store(container=d)

            with self.assertRaises(ValueError):
                store.read('nofile.txt')

    def test_raise_valueerror_on_not_found_on_subdir(self):
        """
        If the file does not exist on a subdirectory, it should raise
        ``ValueError``.
        """
        with self.make_container() as d:
            store = self.get_store(container=d)

            with self.assertRaises(ValueError):
                store.read('a/b/c/nofile.txt')

    def test_read_absolute_paths(self):
        """
        The store should resolve paths that are "absolute" - i.e., start with
        a slash.
        """
        with self.make_container() as d, \
                self.make_document(
                    'sub.txt', where=d, path='a/b/c', content='subdir') as f:

            store = self.get_store(container=d)
            self.assertEquals('subdir', store.read('/a/b/c/sub.txt'))
