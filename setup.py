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

from setuptools import setup, find_packages

setup(
    name="confeitaria-static",
    version="0.0.1.dev1",
    author='Adam Victor Brandizzi',
    author_email='adam@brandizzi.com.br',
    description='confeitaria-static',
    license='LGPLv3',
    url='http://bitbucket.com/brandizzi/confeitaria-static',

    packages=find_packages(),
    install_requires=['confeitaria'],
    test_suite='confeitaria_static_tests',
    test_loader='unittest:TestLoader',
    tests_require=['inelegant', 'requests']
)
