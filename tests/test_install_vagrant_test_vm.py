#!/usr/bin/env python2.7


"""
Testing of install vagrant test vm playbook.
   Craig J Perry <craigp84@gmail.com>
"""


from os.path import abspath, join, dirname, pardir
from tests.playbook_testing_framework import AnsiblePlayTestCase
from tests.playbook_testing_framework.mixins import PackageAssertsMixin, FileSystemAssertsMixin
from tests.playbook_testing_framework.helpers import remove_package


class TestInstallVagrantVM(AnsiblePlayTestCase, PackageAssertsMixin, FileSystemAssertsMixin):

    PLAYBOOK = abspath(join(dirname(__file__), pardir, "install-vagrant-test-vm.yml"))

    def test_case_setup_correctly(self):
        self.assert_file_exists(self.PLAYBOOK)

    def test_installs_git(self):
        remove_package("git", force=True)
        self.assert_package_not_installed("git")
        self.play()
        self.assert_package_installed("git")

    def test_inserts_hostname_alias_in_hosts_file(self):
        self.play()
        self.assert_file_contains("/etc/hosts", 1, "127.0.0.1.*vagrant-fedora-19")

