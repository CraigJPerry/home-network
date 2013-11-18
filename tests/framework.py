#!/usr/bin/env python2.7


"""
Lightweight library for testing ansible playbooks.
   Craig J Perry <craigp84@gmail.com>
"""


import os
import re
import unittest
import subprocess
from os.path import dirname, join, abspath, pardir, exists, isfile, isdir, islink
from tempfile import TemporaryFile


FIXTURES_DIR = abspath(join(dirname(__file__), "fixtures"))
ROOT_DIR = abspath(join(dirname(__file__), pardir))


class Pep8TestCase(unittest.TestCase):
    "Improve consistency by exposing PEP8 compliant test func names"

    assert_equal = unittest.TestCase.assertEqual
    assert_raises = unittest.TestCase.assertRaises
    assert_true = unittest.TestCase.assertTrue
    assert_in = unittest.TestCase.assertIn


class SudoError(Exception):
    pass


def _sudo(cmdline, expected_return_codes=[]):
    """Run cmdline via sudo.

    Return True if return code 0, False if return code 1. Any other
    return code raises SudoError"""
    if not hasattr(cmdline, '__iter__'):
        cmdline = [cmdline]
    if not expected_return_codes:
        expected_return_codes = [1]

    if not os.geteuid() == 0:
        cmdline = ["/usr/bin/sudo"] + cmdline

    with TemporaryFile() as stdout_stderr:
        try:
            return_code = subprocess.check_call(cmdline, stdout=stdout_stderr, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            if ex.returncode in expected_return_codes:
                return False
            else:
                stdout_stderr.seek(0)
                output = stdout_stderr.read()
                msg = "Failed to run command [%s] because [%s]" % (
                        cmdline, output.replace("\n", " "))
                raise SudoError(msg)
        else:
            return True


def install_package(package_names):
    "Yum install package(s)"
    if not hasattr(package_names, '__iter__'):
        package_names = [package_names]

    cmdline = ["/usr/bin/yum", "-y", "install"] + package_names
    return _sudo(cmdline)


def remove_package(package_names, force=False):
    "Return True if uninstalled, False if already uninstalled"
    if not hasattr(package_names, '__iter__'):
        package_names = [package_names]

    cmdline = ["/usr/bin/rpm", "-e"] + package_names
    if force:
        cmdline.append("--nodeps")

    return _sudo(cmdline)


def remove_user(usernames):
    "Return True if removed, False if wasn't present already"
    if not hasattr(usernames, '__iter__'):
        usernames = [usernames]

    cmdline = ["/sbin/userdel"] + usernames
    return _sudo(cmdline, expected_return_codes = [6])


def add_user(username):
    "Convenience func to add user account"
    cmdline = ["/sbin/useradd", username]
    return _sudo(cmdline, expected_return_codes = [4, 9])


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

