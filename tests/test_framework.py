#!/usr/bin/env python2.7


"""
Testing of the "Ansible Testing Framework" itself.
   Craig J Perry <craigp84@gmail.com>
"""


import unittest
from os.path import join
from StringIO import StringIO
from tests.framework import FileSystemAssertsMixin, Pep8TestCase, AnsiblePlayTestCase, AnsiblePlaybookError, FIXTURES_DIR, PackageAssertsMixin, remove_package, install_package, remove_user, add_user, SudoError


class TestFileSystemAssertsMixinExists(Pep8TestCase, FileSystemAssertsMixin):

    def test_file_exists(self):
        self.assert_file_exists(__file__)

    def test_exist_fails_when_file_doesnt_exist(self):
        self.assert_raises(AssertionError, self.assert_file_exists, "this-file-doesnt-exist")

    def test_file_doesnt_exist(self):
        self.assert_file_doesnt_exist("foo")

    def test_doesnt_exist_fails_when_file_does_exist(self):
        self.assert_raises(AssertionError, self.assert_file_doesnt_exist, __file__)


class TestFileSystemAssertsMixinContains(Pep8TestCase, FileSystemAssertsMixin):

    def test_file_contains(self):
        self.assert_file_contains("/etc/passwd", 1, "^root")

    def test_file_contains_multiple_on_one_line_plus_matches_on_other_lines(self):
        self.assert_file_contains("/etc/passwd", 4, "root")

    def test_file_not_containing_expected_regex_fails(self):
        self.assert_raises(AssertionError, self.assert_file_contains, "/etc/passwd", 1, "root")

    def test_file_doesnt_contain(self):
        self.assert_file_doesnt_contain("/etc/passwd", "DonkeyKongRacer")

    def test_file_unexpectedly_containing_regex_fails(self):
        self.assert_raises(AssertionError, self.assert_file_doesnt_contain, "/etc/passwd", "root")


class TestAnsiblePlayTestCase(AnsiblePlayTestCase):

    PLAYBOOK = join(FIXTURES_DIR, "TestAnsiblePlayTestCase.yml")

    def test_can_invoke_playbook(self):
        output = self.play()
        self.assert_in('ok: [10.78.19.84] => {"msg": "Hello, World!"}', output)

    def test_play_output_is_broken_into_list_of_lines(self):
        output = self.play()
        self.assert_true(type(output) is list)

    def test_INVENTORY_exists(self):
        self.assert_file_exists(self.INVENTORY, "file")


class TestNonExistantPlaybook(AnsiblePlayTestCase):

    PLAYBOOK = "DoesntExist.yml"

    def test_play_invocation_flags_failure_to_test_framework(self):
        self.assert_raises(AnsiblePlaybookError, self.play)

    def test_exception_contains_return_code(self):
        try:
            self.play()
        except AnsiblePlaybookError as ex:
            self.assert_in("return code [1]", ex.message)
        else:
            self.fail("Exception wasn't raised for failed ansible-playbook run")

    def test_exception_contains_reason(self):
        try:
            self.play()
        except AnsiblePlaybookError as ex:
            self.assert_in("because [ERROR: the playbook: DoesntExist.yml could not be found]", ex.message)
        else:
            self.fail("Exception wasn't raised for failed ansible-playbook run")


class TestPackageAssertsMixinNotInstalled(Pep8TestCase, PackageAssertsMixin):

    def test_package_not_installed(self):
        self.assert_package_not_installed("non-existant-package-name")

    def test_accepts_list_of_packages(self):
        self.assert_package_not_installed(["doesnt-exist-1", "doesnt-exist-2"])

    def test_raises_when_package_is_installed(self):
        self.assert_raises(AssertionError, self.assert_package_not_installed, "bash")

    def test_raises_when_one_package_is_installed(self):
        self.assert_raises(AssertionError, self.assert_package_not_installed, ['not-installed', 'bash'])


class TestPackageAssertsMixinInstalled(Pep8TestCase, PackageAssertsMixin):

    def test_package_installed(self):
        self.assert_package_installed("bash")

    def test_accepts_list_of_packages(self):
        self.assert_package_installed(["bash", "kernel"])

    def test_raises_when_package_not_installed(self):
        self.assert_raises(AssertionError, self.assert_package_installed, "not-installed")

    def test_raises_when_one_package_not_installed(self):
        self.assert_raises(AssertionError, self.assert_package_installed, ['not-installed', 'bash'])


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

