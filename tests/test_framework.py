#!/usr/bin/env python2.7


"""
Testing of the "Ansible Testing Framework" itself.
   Craig J Perry <craigp84@gmail.com>
"""


import unittest
from os.path import join
from StringIO import StringIO
from tests.framework import FileSystemAssertsMixin, Pep8TestCase, AnsiblePlayTestCase, AnsiblePlaybookError, FIXTURES_DIR, PackageAssertsMixin, remove_package, install_package, remove_user, add_user, SudoError


class TestRemovePackage(Pep8TestCase, PackageAssertsMixin):

    PACKAGE = "libtiff"
    DEPENDENCY = "libtiff-devel"

    def test_can_remove_installed_package(self):
        install_package(self.PACKAGE)
        remove_package(self.DEPENDENCY)
        self.assert_true(remove_package(self.PACKAGE))

    def test_removing_missing_package_does_not_raise(self):
        remove_package(self.PACKAGE)
        self.assert_equal(False, remove_package(self.PACKAGE))

    def test_cant_remove_package_with_remaining_dependencies(self):
        install_package(self.PACKAGE)
        install_package(self.DEPENDENCY)
        self.assert_equal(False, remove_package(self.PACKAGE))

    def test_can_force_remove_package_with_remaining_dependencies(self):
        install_package(self.PACKAGE)
        install_package(self.DEPENDENCY)
        self.assert_true(remove_package(self.PACKAGE, force=True))


class TestInstallPackage(Pep8TestCase, PackageAssertsMixin):

    PACKAGE = "libtiff"

    def test_can_install_package(self):
        install_package(self.PACKAGE)
        self.assert_package_installed(self.PACKAGE)

    def test_installing_already_installed_does_not_raise(self):
        install_package(self.PACKAGE)
        self.assert_equal(True, install_package(self.PACKAGE))


class TestRemoveUser(Pep8TestCase, FileSystemAssertsMixin):

    def test_can_remove_user(self):
        add_user("testingremoval")
        self.assert_file_contains("/etc/passwd", 1, "^testingremoval")
        remove_user("testingremoval")
        self.assert_file_doesnt_contain("/etc/passwd", "^testingremoval")

    def test_removing_non_existant_user_does_not_raise_exception(self):
        try:
            remove_user("doesnt-exist")
        except SudoError as ex:
            self.fail("User removal triggered unexpected return code")


class TestAddUser(Pep8TestCase, FileSystemAssertsMixin):

    def test_can_add_user(self):
        remove_user("test-add-user")
        self.assert_file_doesnt_contain("/etc/passwd", "test-add-user")
        add_user("test-add-user")
        self.assert_file_contains("/etc/passwd", 1, "^test-add-user")

    def test_adding_existing_user_does_not_raise_exception(self):
        try:
            add_user("already-present")
            add_user("already-present")
        except SudoError as ex:
            self.fail("Repeated user addition resulted in an unexpected return code")

