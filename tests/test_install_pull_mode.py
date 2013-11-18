#!/usr/bin/env python2.7


"""
Testing of install-pull-mode playbook.
   Craig J Perry <craigp84@gmail.com>
"""


import unittest
from os.path import join, dirname, pardir
from tests.framework import AnsiblePlayTestCase, PackageAssertsMixin, remove_package, remove_user
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
        self.assert_file_contains("/etc/passwd", 1, "^ansible:x:[0-9]+:[0-9]+:Ansible Configuration Management:/home/ansible:/bin/bash")

    def test_repairs_ansible_user(self):
        remove_user("ansible")
        add_user("ansible")  # This user entry won't match definition in playbook
        self.play()
        self.assert_file_contains("/etc/passwd", 1, "^ansible:x:[0-9]+:[0-9]+:Ansible Configuration Management:/home/ansible:/bin/bash")

    def test_disables_requiretty_for_ansible_sudoers_entry(self):
        self.play()
        self.assert_file_contains("/etc/sudoers.d/ansible", 1, "^Defaults: ansible !requiretty$")

    def test_enables_sudoers_rule_for_ansible(self):
        self.play()
        self.assert_file_contains("/etc/sudoers.d/ansible", 1, "^ansible ALL=(ALL) NOPASSWD: ALL$")


@unittest.skipUnless(getuser() != "root", "Requires non-root user for accurate testing")
class TestInstallAsNonRootViaSudo(InstallPullModeTestCases, AnsiblePlayTestCase, PackageAssertsMixin):
    pass


@unittest.skipUnless(getuser() == "root", "Requires root user for accurate testing")
class TestInstallAsRoot(InstallPullModeTestCases, AnsiblePlayTestCase, PackageAssertsMixin):

    def test_creates_ansible_pull_crontab_entry(self):
        self.play()
        self.assert_file_contains("/var/spool/cron/ansible", 1, "^@hourly ansible-pull")

    def test_removes_installer_cronjob_inserted_by_kickstart(self):
        with open("/etc/cron.d/ansible-pull-install", "w") as cronjob:
            cronjob.write("This is just a dummy testing example")
        self.play()
        self.assert_file_doesnt_exist("/etc/cron.d/ansible-pull-install")

