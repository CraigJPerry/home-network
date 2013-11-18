#!/usr/bin/env python2.7


"""
Lightweight library for testing ansible playbooks.
   Craig J Perry <craigp84@gmail.com>
"""


import unittest
import subprocess
from os.path import dirname, join, abspath, pardir
from .playbook_testing_framework.mixins import FileSystemAssertsMixin


ROOT_DIR = abspath(join(dirname(__file__), pardir))


class Pep8TestCase(unittest.TestCase):
    "Improve consistency by exposing PEP8 compliant test func names"

    assert_equal = unittest.TestCase.assertEqual
    assert_raises = unittest.TestCase.assertRaises
    assert_true = unittest.TestCase.assertTrue
    assert_in = unittest.TestCase.assertIn


class AnsiblePlaybookError(Exception):
    "Any error signaled by ansible-playbook failing to complete normally"
    pass


class AnsiblePlayTestCase(Pep8TestCase, FileSystemAssertsMixin):
    """TestCase for ansible play testing.

    Subclass this rather than unittest.TestCase when writing tests for
    ansible playbooks.

    Redefine cls.PLAYBOOK with the path to the playbook to be tested.

    Write test_xxx() methods as normal. Group related tests in their own
    subclasses of AnsiblePlayTestCase.

    Call the self.play() method in your tests to invoke the playbook,
    all ansible output on stdout or stderr will be returned from this
    call.

    Use the PEP8-compliant assert methods in your tests:

    * assert_true
    * assert_equal
    * assert_in
    * assert_raises
    * assert_file_exists
    * assert_file_doesnt_exist
    * assert_file_contains
    * assert_file_doesnt_contain

    A failure in the ``ansible-playbook`` run with raise
    AnsiblePlaybookError.
    """

    INVENTORY = join(ROOT_DIR, "hosts-testing")
    PLAYBOOK = ""

    def play(self):
        "Invoke the playbook associated with this TestCase"

        cmdline = ["ansible-playbook", "--connection=local", "--inventory-file=" + self.INVENTORY, self.PLAYBOOK]
        output = ""

        try:
            output = subprocess.check_output(cmdline, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            msg = "ansible-playbook failed with return code [{0}] because [{1}]".format(ex.returncode, ex.output.strip())
            raise AnsiblePlaybookError(msg)

        return output.splitlines()

