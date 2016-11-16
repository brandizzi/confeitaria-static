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
from confeitaria.static.store.aggregate import AggregateStore

from confeitaria_static_tests.store.reference import ReferenceStoreTestCase
from confeitaria_static_tests.store.fake import available_document


class TestAggregateStore(unittest.TestCase):

    def test_get_from_primary_store(self):
        """
        If the primary store can provide the content, then it should,
        regardless of what the secondary store could do.
        """
        primary = FakeStore({'test.html': 'primary content'})
        secondary = FakeStore({'test.html': 'secondary_store content'})

        aggregate = AggregateStore(primary, secondary)

        self.assertEquals(
            primary.read('test.html'), aggregate.read('test.html'))


class ReferenceAggregateStoreTestCase(ReferenceStoreTestCase):

    def get_store(self, container, default_file_name='index.html'):
        """
        Create an aggregate store which will hold two fake stores.

        * ``container`` is a tuple with two dicts. The first dict is to be
           given to the primary store of the aggregate store, and the second
           one is the argument of the secondary story.
        """
        primary, secondary = container

        primary_store = FakeStore(
            documents=primary, default_file_name=default_file_name)
        secondary_store = FakeStore(
            documents=secondary, default_file_name=default_file_name)

        return AggregateStore(primary_store, secondary_store)

    @contextlib.contextmanager
    def make_container(self):
        """
        Yields a tuple with two dicts. The first one is to be given as argument
        to the primary fake store from the aggregate. The second one will then
        hold th the mappings of the secondary fake store.
        """
        yield {}, {}


class ReferenceTestPrimaryInAggregateStore(ReferenceAggregateStoreTestCase):

    def make_document(self, name, where, content='', path=None):
        """
        This case tests the aggregate store but sets up the primary store of
        the aggregate in every test from ``ReferenceStoreTestCase``. This way,
        any request to the secondary store will fail, and requests to the
        primary store will behave as expected by the refernece tests. So, this
        test case ensures that, whenever the primary store can provide some
        content, it will provide, regardless of the secondary story.
        """
        primary, _ = where

        return available_document(primary, name, content, path=path)


class ReferenceTestSecondaryInAggregateStore(ReferenceAggregateStoreTestCase):

    def make_document(self, name, where, content='', path=None):
        """
        This case tests the aggregate store but sets up the secondary store of
        the aggregate in every test from ``ReferenceStoreTestCase``. This way,
        any request to the primary store will fail and the aggregate store will
        have to reach the secondary one.. So, this test case ensures that,
        whenever the primary store failsto provide some content, the secondary
        will provide it if it can.
        """
        _, secondary = where

        return available_document(secondary, name, content, path=path)


load_tests = TestFinder(
    __name__,
    'confeitaria.static.store.aggregate',
    skip=[ReferenceStoreTestCase, ReferenceAggregateStoreTestCase]
).load_tests

if __name__ == '__main__':
    unittest.main()
