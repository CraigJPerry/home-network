#!/usr/bin/env python


"""
Testing of Ansible playbooks.
   Craig J Perry <craigp84@gmail.com>
"""


import sys
import re
import unittest
from os.path import dirname, join, abspath, exists, isfile, isdir, islink
from sh import ansible_playbook
from StringIO import StringIO


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

    def assertFileContains(self, filepath, count, regex):
        "Check if filepath contains count occurances of regex"
        with open(filepath, "r") as fhandle:
            matches = sum(len(re.findall(regex, line)) for line in fhandle.xreadlines())
        self.assertEqual(count, matches)

    def assertFileDoesntContain(self, filepath, regex):
        return self.assertFileContains(filepath, 0, regex)


class TestFileSystemAssertsMixin(unittest.TestCase, FileSystemAssertsMixin):

    def test_file_exists(self):
        self.assertFileExists(__file__)

    def test_file_doesnt_exist(self):
        self.assertFileNotExists("foo")

    def test_file_contains(self):
        self.assertFileContains("/etc/passwd", 4, "root")
        self.assertFileContains("/etc/passwd", 1, "^root")

    def test_file_doesnt_contain(self):
        self.assertFileDoesntContain("/etc/passwd", "DonkeyKongRacer")


class AnsiblePlayTestCase(unittest.TestCase, FileSystemAssertsMixin):
    "TestCase for ansible play testing"

    FIXTURES_DIR = abspath(join(dirname(__file__), "fixtures"))

    def play(self, playbook, logfile="/dev/null"):
        playbook_path = join(self.FIXTURES_DIR, playbook)
        ansible_playbook(playbook_path, inventory_file="localhost,", _out=logfile, _err=logfile)

class TestAnsiblePlayTestCase(AnsiblePlayTestCase):

    def test_can_invoke_playbook(self):
        logfile = StringIO()
        self.play("TestAnsiblePlayTestCase.yml", logfile)
        logfile.seek(0)
        self.assertIn('ok: [localhost] => {"msg": "Hello, World!"}', logfile.read())

