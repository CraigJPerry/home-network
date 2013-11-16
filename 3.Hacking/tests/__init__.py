#!/usr/bin/env python


"""
Testing of Ansible playbooks.
   Craig J Perry <craigp84@gmail.com>
"""


import sys
from os.path import dirname, join, abspath


def setUpPackage():
    "Ensure tests package is importable from within tests"
    sys.path.insert(0, abspath(join(dirname(__file__), "..")))


