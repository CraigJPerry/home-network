#!/usr/bin/env python


"""
Lightweight library for testing ansible playbooks.
   Craig J Perry <craigp84@gmail.com>
"""


import re
import unittest
import subprocess
from os.path import dirname, join, abspath, exists, isfile, isdir, islink


class Pep8TestCase(unittest.TestCase):
    "Improve consistency by exposing PEP8 compliant test func names"

    assert_equal = unittest.TestCase.assertEqual
    assert_raises = unittest.TestCase.assertRaises
    assert_true = unittest.TestCase.assertTrue


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


class AnsiblePlayTestCase(Pep8TestCase, FileSystemAssertsMixin):
    "TestCase for ansible play testing"

    FIXTURES_DIR = abspath(join(dirname(__file__), "fixtures"))
    INVENTORY = join(FIXTURES_DIR, "testing-inventory")
    PLAYBOOK = ""

    def play(self):
        cmdline = ["ansible-playbook", "--connection=local", "--inventory-file=" + self.INVENTORY, self.PLAYBOOK]
        output = ""
        try:
            output = subprocess.check_output(cmdline, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            msg = "ansible-playbook failed with return code [{0}] because [{1}]".format(ex.returncode, ex.output)
            self.fail(msg)
        return output.splitlines()

