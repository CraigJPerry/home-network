#!/usr/bin/env python2.7


"""
Lightweight library for testing ansible playbooks.
   Craig J Perry <craigp84@gmail.com>
"""


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
        "Check if filepath has 0 occurences of regex"
        return self.assert_file_contains(filepath, 0, regex)


class PackageAssertsMixin(object):
    "TestCase mixin giving assertions about the system packaging DB"

    def assert_package_not_installed(self, package_names):
        "Check if a package, or list of packages, are not installed"
        if not hasattr(package_names, '__iter__'):
            package_names = [package_names]

        for pkg in package_names:
            self.assert_true(not self._rpm_installed(pkg))

    def assert_package_installed(self, package_names):
        "Check if a package, or list of packages, are installed"

        if not hasattr(package_names, '__iter__'):
            package_names = [package_names]

        for pkg in package_names:
            self.assert_true(self._rpm_installed(pkg))

    def _rpm_installed(self, package_name):
        cmdline = ["/usr/bin/rpm", "-q", package_name]
        return _sudo(cmdline)


class SudoError(Exception):
    pass


def _sudo(cmdline):
    """Run cmdline via sudo.

    Return True if return code 0, False if return code 1. Any other
    return code raises SudoError"""
    cmdline = ["/usr/bin/sudo"] + cmdline

    with TemporaryFile() as stdout_stderr:
        try:
            return_code = subprocess.check_call(cmdline, stdout=stdout_stderr, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            if ex.returncode == 1:
                return False
            else:
                stdout_stderr.seek(0)
                output = stdout_stderr.read()
                msg = "Failed to run command [%s] because [%s]" % (
                        cmdline, output.replace("\n", " "))
                raise PackageManagerError(msg)
        else:
            return True


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

