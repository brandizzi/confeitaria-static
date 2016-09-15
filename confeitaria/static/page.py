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

import confeitaria.interfaces


class StaticPage(confeitaria.interfaces.Page):

    def __init__(self, directory):
        self.directory = directory

    def index(self, path):
        try:
            path = os.path.join(self.directory, path)
        except TypeError:
            path = ''

        with open(path) as f:
            content = f.read()

        return content
