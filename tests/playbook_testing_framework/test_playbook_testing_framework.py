#!/usr/bin/env python2.7


"""
Testing of the "Ansible Testing Framework" itself.
   Craig J Perry <craigp84@gmail.com>
"""


from os.path import join, dirname, abspath
from tests.playbook_testing_framework import AnsiblePlayTestCase, AnsiblePlaybookError
from tests.playbook_testing_framework.mixins import FileSystemAssertsMixin


class TestAnsiblePlayTestCaseContract(AnsiblePlayTestCase, FileSystemAssertsMixin):

    PLAYBOOK = abspath(join(dirname(__file__), "TestAnsiblePlayTestCase.yml"))

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

