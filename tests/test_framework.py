#!/usr/bin/env python2.7


"""
Testing of the "Ansible Testing Framework" itself.
   Craig J Perry <craigp84@gmail.com>
"""


import unittest
from os.path import join
from StringIO import StringIO
from tests.framework import FileSystemAssertsMixin, Pep8TestCase, AnsiblePlayTestCase, AnsiblePlaybookError, FIXTURES_DIR


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

