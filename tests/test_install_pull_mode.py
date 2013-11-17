#!/usr/bin/env python2.7


"""
Testing of install-pull-mode playbook.
   Craig J Perry <craigp84@gmail.com>
"""


from os.path import join, dirname, pardir
from tests.framework import AnsiblePlayTestCase
from getpass import getuser


class TestInstallAsNonRootViaSudo(AnsiblePlayTestCase):

    PLAYBOOK = join(dirname(__file__), pardir, "install-pull-mode.yml")

    def test_case_setup_correctly(self):
        self.assert_true(getuser() != "root")
        self.assert_file_exists(self.PLAYBOOK)

