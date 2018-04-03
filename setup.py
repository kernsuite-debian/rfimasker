#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 SKA South Africa
#
# This file is part of RFIMasker.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import os
from setuptools import setup

pkg='RFIMasker'

build_root=os.path.dirname(__file__)

def get_version():
    # Versioning code here, based on
    # http://blogs.nopcode.org/brainstorm/2013/05/20/pragmatic-python-versioning-via-setuptools-and-git-tags/

    # Fetch version from git tags, and write to version.py.
    # Also, when git is not available (PyPi package), use stored version.py.
    version_py = os.path.join(build_root, pkg, 'version.py')

    try:
        version_git = subprocess.check_output(['git', 'describe', '--tags']).rstrip()
    except:
        with open(version_py, 'r') as fh:
            version_git = open(version_py).read().strip().split('=')[-1].replace('"','')

    version_msg = "# Do not edit this file, pipeline versioning is governed by git tags"

    with open(version_py, 'w') as fh:
        fh.write(version_msg + os.linesep + "__version__=\"" + version_git +"\"")

    return version_git

def readme():
    with open(os.path.join(build_root, 'README.md')) as f:
        return f.read()

def src_pkg_dirs(pkg_name):
    mbdir = os.path.join(build_root, pkg_name)
    # Ignore
    pkg_dirs = []
    l = len(mbdir) + len(os.sep)
    exclude = ['docs', '.git', '.svn', 'CMakeFiles']
    for root, dirs, files in os.walk(mbdir, topdown=True):
        # Prune out everything we're not interested in
        # from os.walk's next yield.
        dirs[:] = [d for d in dirs if d not in exclude]

        for d in dirs:
            # OK, so everything starts with 'RFIMasker/'
            # Take everything after that ('src...') and
            # append a '/*.*' to it
            pkg_dirs.append(os.path.join(root[l:], d, '*.*'))
    return pkg_dirs

def define_scripts():
    #these must be relative to setup.py according to setuputils
    return [os.path.join(pkg,"scripts",script_name) for script_name in ["mask_ms.py"]]

setup(name=pkg,
      version=get_version(),
      description='Tool to apply rfi masks to measurement sets',
      long_description=readme(),
      url='https://github.com/bennahugo/RFIMasker',
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Astronomy"],
      author='Benjamin Hugo',
      author_email='bhugo@ska.ac.za',
      license='GNU GPL v2',
      packages=[pkg],
      install_requires=[
          "numpy==1.13.3",
          "scipy==1.0.0",
          "python-casacore==2.1.2"
      ],
      package_data={pkg: src_pkg_dirs(pkg)},
      include_package_data=True,
      zip_safe=False,
      scripts=define_scripts()
)
