#!/usr/bin/env python2.7


"""
Testing of install-pull-mode playbook.
   Craig J Perry <craigp84@gmail.com>
"""


import unittest
from os.path import join, dirname, pardir
from tests.framework import AnsiblePlayTestCase, PackageAssertsMixin, remove_package
from getpass import getuser


class InstallPullModeTestCases(object):

    PLAYBOOK = join(dirname(__file__), pardir, "install-pull-mode.yml")

    def test_case_setup_correctly(self):
        self.assert_file_exists(self.PLAYBOOK)

    def test_installs_git(self):
        remove_package("git", force=True)
        self.assert_package_not_installed("git")
        self.play()
        self.assert_package_installed("git")

    def test_creates_ansible_user(self):
        remove_user("ansible")
        self.assert_file_doesnt_contain("/etc/passwd", "^ansible")
        self.play()
        self.assert_file_contains("/etc/passwd", "^ansible:x:[0-9]+:[0-9]+:Ansible Configuration Management:/home/ansible:/bin/bash")

    def test_repairs_ansible_user(self):
        remove_user("ansible")
        with open("/etc/passwd", "w") as passwd:
            passwd.write("ansible:x:996:996:Wrong comment text:/not/ansibles/home:/bin/false\n")
        self.play()
        self.assert_file_contains("/etc/passwd", "^ansible:x:[0-9]+:[0-9]+:Ansible Configuration Management:/home/ansible:/bin/bash")

    def test_disables_requiretty_for_ansible_sudoers_entry(self):
        self.play()
        self.assert_file_contains("/etc/sudoers.d/ansible", 1, "Defaults: ansible !requiretty")


@unittest.skipUnless(getuser() != "root", "Requires non-root user for accurate testing")
class TestInstallAsNonRootViaSudo(InstallPullModeTestCases, AnsiblePlayTestCase, PackageAssertsMixin):
    pass


@unittest.skipUnless(getuser() == "root", "Requires root user for accurate testing")
class TestInstallAsRoot(InstallPullModeTestCases, AnsiblePlayTestCase, PackageAssertsMixin):
    pass

