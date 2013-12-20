#!/usr/bin/env python2.7


"""
Testing of lan role.
   Craig J Perry <craigp84@gmail.com>
"""


import unittest
from os.path import join
from .framework import AnsiblePlayTestCase
from .framework.mixins import PackageAssertsMixin, FileSystemAssertsMixin
from .framework.helpers import remove_package


class Network(AnsiblePlayTestCase, PackageAssertsMixin, FileSystemAssertsMixin):

    PLAYBOOK = join(AnsiblePlayTestCase.FIXTURES_DIR, "lan.yml")

    def test_setup_correctly(self):
        self.assert_file_exists(self.PLAYBOOK)

    def test_installs_nss_mdns(self):
        remove_package("nss-mdns", force=True)
        self.assert_package_not_installed("nss-mdns")
        self.play()
        self.assert_package_installed("nss-mdns")

    def test_installs_avahi_tools(self):
        remove_package("avahi-tools", force=True)
        self.assert_package_not_installed("avahi-tools")
        self.play()
        self.assert_package_installed("avahi-tools")


class Users(AnsiblePlayTestCase, PackageAssertsMixin, FileSystemAssertsMixin):

    PLAYBOOK = join(AnsiblePlayTestCase.FIXTURES_DIR, "lan.yml")

    def test_setup_correctly(self):
        self.assert_file_exists(self.PLAYBOOK)


if __name__ == "__main__":
    unittest.main()

