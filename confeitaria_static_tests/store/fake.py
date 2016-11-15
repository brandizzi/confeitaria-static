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
import contextlib

from inelegant.finder import TestFinder

from confeitaria.static.store.fake import FakeStore

from confeitaria_static_tests.store.reference import ReferenceStoreTestCase


class ReferenceTestFileStore(ReferenceStoreTestCase):

    def get_store(self, container, default_file_name='index.html'):
        """
        Create a file store with the given arguments.
        """
        return FakeStore(
            documents=container, default_file_name=default_file_name)

    @contextlib.contextmanager
    def make_container(self):
        """
        Yields a dict where the documents will be added.
        """
        yield {}

    def make_document(self, name, where, content='', path=None):
        """
        Adds a new document to the dict of documents.
        """
        return available_document(where, path, name, content)


@contextlib.contextmanager
def available_document(document_dict, path, name, content):
    if path is not None:
        path = os.path.join(path, name)
    else:
        path = name

    previous_content = document_dict.get(path, None)
    document_dict[path] = content

    try:
        yield
    finally:
        del document_dict[path]

        if previous_content is not None:
            document_dict[path] = previous_content


load_tests = TestFinder(
    __name__,
    'confeitaria.static.store.fake',
    skip=ReferenceStoreTestCase
).load_tests

if __name__ == '__main__':
    unittest.main()
