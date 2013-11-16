#!/usr/bin/env python2.7


"""
Testing of "Ansible Testing Framework" itself.
   Craig J Perry <craigp84@gmail.com>
"""


from os.path import join
from StringIO import StringIO
from tests import FileSystemAssertsMixin, Pep8TestCase, AnsiblePlayTestCase


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

    PLAYBOOK = join(AnsiblePlayTestCase.FIXTURES_DIR, "simple-echo.yml")

    def test_can_invoke_playbook(self):
        output = self.play()
        self.assertIn('ok: [localhost] => {"msg": "Hello, World!"}', output)

