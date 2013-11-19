#!/usr/bin/env python2.7


"""
Testing of install vagrant test vm playbook.
   Craig J Perry <craigp84@gmail.com>
"""


from os.path import abspath, join, dirname, pardir
from tests.playbook_testing_framework import AnsiblePlayTestCase
from tests.playbook_testing_framework.mixins import PackageAssertsMixin
from tests.playbook_testing_framework.helpers import remove_package


class TestInstallVagrantVM(AnsiblePlayTestCase, PackageAssertsMixin):

    PLAYBOOK = abspath(join(dirname(__file__), pardir, "install_vagrant_test_vm.yml"))

    def test_case_setup_correctly(self):
        self.assert_file_exists(self.PLAYBOOK)

    def test_installs_git(self):
        remove_package("git", force=True)
        self.assert_package_not_installed("git")
        self.play()
        self.assert_package_installed("git")

