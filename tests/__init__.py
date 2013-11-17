#!/usr/bin/env python2.7


"""
Lightweight library for testing ansible playbooks.
   Craig J Perry <craigp84@gmail.com>
"""


import re
import unittest
import subprocess
from os.path import dirname, join, abspath, pardir, exists, isfile, isdir, islink


FIXTURES_DIR = abspath(join(dirname(__file__), "fixtures"))
ROOT_DIR = abspath(join(dirname(__file__), pardir))


class Pep8TestCase(unittest.TestCase):
    "Improve consistency by exposing PEP8 compliant test func names"

    assert_equal = unittest.TestCase.assertEqual
    assert_raises = unittest.TestCase.assertRaises
    assert_true = unittest.TestCase.assertTrue


class FileSystemAssertsMixin(object):
    "Mix this class into your TestCase to get some file system assertions"

    def assert_file_exists(self, filepath, kind="any"):
        "Check if filepath exists and is a <file|dir|link>"

        self.assert_true(exists(filepath))

        if "file" in kind.lower():
            self.assert_true(isfile(filepath))
        elif "dir" in kind.lower():
            self.assert_true(isdir(filepath))
        elif "link" in kind.lower():
            self.assert_true(islink(filepath))

    def assert_file_doesnt_exist(self, filepath):
        "Confirm filepath doesn't exist"
        self.assert_true(not exists(filepath))

    def assert_file_contains(self, filepath, count, regex):
        "Check if filepath contains count occurances of regex"

        with open(filepath, "r") as fhandle:
            matches = sum(len(re.findall(regex, line)) for line in fhandle.xreadlines())
        self.assert_equal(count, matches)

    def assert_file_doesnt_contain(self, filepath, regex):
        return self.assert_file_contains(filepath, 0, regex)


class AnsiblePlaybookError(Exception):
    pass


class AnsiblePlayTestCase(Pep8TestCase, FileSystemAssertsMixin):
    "TestCase for ansible play testing"

    INVENTORY = join(ROOT_DIR, "hosts-testing")
    PLAYBOOK = ""

    def play(self):
        cmdline = ["ansible-playbook", "--connection=local", "--inventory-file=" + self.INVENTORY, self.PLAYBOOK]
        output = ""
        try:
            output = subprocess.check_output(cmdline, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            msg = "ansible-playbook failed with return code [{0}] because [{1}]".format(ex.returncode, ex.output.strip())
            raise AnsiblePlaybookError(msg)
        return output.splitlines()

