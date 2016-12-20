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
from inelegant.dict import temp_key

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
        return available_document(where, name, content, path=path)


def available_document(document_dict, name, content, path=None):
    """
    ``available_document`` is a context manager that adds a value to a
    dictonary and removes it once its context is exited.

    ``FakeStore`` objects are store implementations that receive their
    "documents" from a dict. ``available_document()`` helps to add a content
    to such a dict. Thsi context manager expects three arguments: the dict,
    the name of the "document" (which will serve as a key) and the content
    which will be the value.

    So, given a dict...

    ::

    >>> d = {}

    ...it will add the given content to the given name::

    >>> with available_document(d, 'test.html', 'example'):
    ...     d
    {'test.html': 'example'}

    Once the context is gone, however, the value will be removed from the
    dict::

    >>> d
    {}

    If the dict was holding another value before...

    ::

    >>> d = {'test.html': 'previous content'}

    ...the value will be restored::

    >>> with available_document(d, 'test.html', 'TEMPORARY content'):
    ...     d
    {'test.html': 'TEMPORARY content'}
    >>> d
    {'test.html': 'previous content'}

    ``available_document()`` can also receive a fourth argument, ``path``. This
    path will be prepended to the name as a URL path::

    >>> with available_document({}, 'test.html', 'content', path='abc') as d:
    ...     d
    {'abc/test.html': 'content'}
    """
    if path is not None:
        path = os.path.join(path, name)
    else:
        path = name

    return temp_key(document_dict, path, content)

load_tests = TestFinder(
    __name__,
    'confeitaria.static.store.fake',
    skip=ReferenceStoreTestCase
).load_tests

if __name__ == '__main__':
    unittest.main()
