#!/usr/bin/env python2.7


"""
Simple test framework to facilitate testing of ansible playbooks.
   Craig J Perry <craigp84@gmail.com>
"""


import unittest
import subprocess
from os.path import dirname, join, abspath, pardir
from .mixins import FileSystemAssertsMixin


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


class AnsiblePlayTestCase(Pep8TestCase):
    """TestCase for ansible play testing.

    Subclass this rather than unittest.TestCase when writing tests for
    ansible playbooks.

    Redefine cls.PLAYBOOK with the path to the playbook to be tested.

    You can write test_xxx() methods as you normally would with python's
    unittest framework. E.g. you can group related tests in their own
    subclasses of AnsiblePlayTestCase.

    Call the self.play() method in your tests to invoke the playbook,
    all ansible output on stdout or stderr will be returned from this
    call. Sometimes it's useful to print this when debugging a play!

    You can use the PEP8-compliant assert methods in your tests:

    * assert_true
    * assert_equal
    * assert_in
    * assert_raises

    And freely mixin assert methods in your TestCase's inheritence tree:

    >>> from playbook_testing_framework import AnsiblePlayTestCase
    >>> from playbook_testing_framework.mixins import FileSystemAssertsMixin
    >>>
    >>> class TestCaseExample(AnsiblePlayTestCase, FileSystemAssertsMixin):
    >>>     def test_something(self):
    >>>         self.assert_file_exists("/path/to/file")  # Time saved!

    See the ``playbook_testing_framework.mixins`` package for more.

    A failure in the ``ansible-playbook`` run will raise
    AnsiblePlaybookError.
    """

    PLAYBOOK = ""  # Set this file path in your subclass
    INVENTORY = join(ROOT_DIR, "hosts-testing")  # Rarely need to override

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

