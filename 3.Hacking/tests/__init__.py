#!/usr/bin/env python


"""
Testing of Ansible playbooks.
   Craig J Perry <craigp84@gmail.com>
"""


import sys
import unittest
from os.path import dirname, join, abspath, exists, isfile, isdir, islink


def setUpPackage():
    "Ensure tests package is importable from within tests"
    sys.path.insert(0, abspath(join(dirname(__file__), "..")))


class FileSystemAssertsMixin(object):
    "Mix this class into your TestCase to get some file system assertions"

    def assertFileExists(self, filepath, kind="any"):
        "Check if filepath exists and is a <file|dir|link>"
        self.assertTrue(exists(filepath))
        if "file" in kind.lower():
            self.assertTrue(isfile(filepath))
        elif "dir" in kind.lower():
            self.assertTrue(isdir(filepath))
        elif "link" in kind.lower():
            self.assertTrue(islink(filepath))

    def assertFileNotExists(self, filepath):
        "Confirm filepath doesn't exist"
        self.assertTrue(not exists(filepath))


class TestFileSystemAssertsMixin(unittest.TestCase, FileSystemAssertsMixin):

    def test_file_exists(self):
        self.assertFileExists(__file__)

    def test_file_doesnt_exist(self):
        self.assertFileNotExists("foo")

