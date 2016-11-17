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


class AggregateStore(object):
    """
    ``AggregateStore`` just delegates the task of reading documents to two
    other stores, a primary one and a secondary one. First, it requests the
    content from the primary store; if this one cannot provide the content,
    aggregate store asks the secondary store for the document.

    An example can make help understanding it. Consider the two fake stores
    below::

    >>> from confeitaria.static.store.fake import FakeStore
    >>> store1 = FakeStore({'test.html': 'FIRST'})
    >>> store2 = FakeStore({'test.html': 'SECOND', 'test2.html': 'SECOND TOO'})

    They both provide a ``test.html`` document, but only the second one can
    serve a ``test2.html``. We can give them to an aggregate store::

    >>> store = AggregateStore(primary=store1, secondary=store2)

    If then we request ``test.html`` from the aggregate store, we will get the
    value from ``store1``, because it is the primary store and  can serve it::

    >>> store.read('test.html')
    'FIRST'

    Now, if we request ``test2.html``, then we will get the value from the
    secondary store ``store2`` because ``store1`` has no such document::

    >>> store.read('test2.html')
    'SECOND TOO'

    Requesting a document that is not available in any of the two stores will
    result in a ``ValueError`` exception::

    >>> store.read('nofile.html')
    Traceback (most recent call last):
      ...
    ValueError: Failed to read nofile.html. Reason: 'nofile.html'
    """

    def __init__(self, primary, secondary):
        self.primary = primary
        self.secondary = secondary

    def read(self, path):
        try:
            content = self.primary.read(path)
        except Exception as e:
            content = self.secondary.read(path)

        return content
