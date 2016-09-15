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
import requests

from inelegant.fs import temp_file, temp_dir

from confeitaria.static.page import StaticPage
from confeitaria.server import Server


class TestStaticPage(unittest.TestCase):

    def test_serve_static_page(self):
        with temp_dir() as d, \
                temp_file(dir=d, name='index.html', content='example') as f:

            page = StaticPage(directory=d)

            with Server(page):
                r = requests.get('http://localhost:8000/index.html')

                self.assertEquals(200, r.status_code)
                self.assertEquals('example', r.text)
