#!/usr/bin/env python2.7


"""
Testing of the "Ansible Testing Framework" itself.
   Craig J Perry <craigp84@gmail.com>
"""


import unittest
from os.path import join
from StringIO import StringIO
from tests.framework import FileSystemAssertsMixin, Pep8TestCase, AnsiblePlayTestCase, AnsiblePlaybookError, FIXTURES_DIR


class TestFileSystemAssertsMixin(Pep8TestCase, FileSystemAssertsMixin):

    def test_file_exists(self):
        self.assert_file_exists(__file__)

    def test_file_doesnt_exist(self):
        self.assert_file_doesnt_exist("foo")

    def test_file_contains(self):
        self.assert_file_contains("/etc/passwd", 4, "root")
        self.assert_file_contains("/etc/passwd", 1, "^root")

    def test_file_doesnt_contain(self):
        self.assert_file_doesnt_contain("/etc/passwd", "DonkeyKongRacer")


class TestAnsiblePlayTestCase(AnsiblePlayTestCase):

    PLAYBOOK = join(FIXTURES_DIR, "TestAnsiblePlayTestCase.yml")

    def test_can_invoke_playbook(self):
        output = self.play()
        self.assertIn('ok: [10.78.19.84] => {"msg": "Hello, World!"}', output)

class TestNonExistantPlaybook(AnsiblePlayTestCase):

    PLAYBOOK = "DoesntExist.yml"

    def test_play_invocation_flags_failure_to_test_framework(self):
        self.assert_raises(AnsiblePlaybookError, self.play)

    def test_exception_contains_return_code(self):
        try:
            self.play()
        except AnsiblePlaybookError as ex:
            self.assertIn("return code [1]", ex.message)
        else:
            self.fail("Exception wasn't raised for failed ansible-playbook run")

    def test_exception_contains_reason(self):
        try:
            self.play()
        except AnsiblePlaybookError as ex:
            self.assertIn("because [ERROR: the playbook: DoesntExist.yml could not be found]", ex.message)
        else:
            self.fail("Exception wasn't raised for failed ansible-playbook run")

