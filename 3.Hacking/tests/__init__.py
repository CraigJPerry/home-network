#!/usr/bin/env python


"""
Testing of Ansible playbooks.
   Craig J Perry <craigp84@gmail.com>
"""


import re
import unittest
from os.path import dirname, join, abspath, exists, isfile, isdir, islink
from sh import ansible_playbook


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


class AnsiblePlayTestCase(unittest.TestCase, FileSystemAssertsMixin):
    "TestCase for ansible play testing"

    FIXTURES_DIR = abspath(join(dirname(__file__), "fixtures"))

    def play(self, playbook, logfile="/dev/null"):
        playbook_path = join(self.FIXTURES_DIR, playbook)
        ansible_playbook(playbook_path, inventory_file="localhost,", _out=logfile, _err=logfile)

