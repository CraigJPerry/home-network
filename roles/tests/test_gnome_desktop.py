#!/usr/bin/env python2.7


"""
Testing of gnome_desktop role.
   Craig J Perry <craigp84@gmail.com>
"""


import unittest
from os.path import join
from .framework import AnsiblePlayTestCase
from .framework.mixins import PackageAssertsMixin, FileSystemAssertsMixin
from .framework.helpers import remove_package


class InstallAnsible(AnsiblePlayTestCase, PackageAssertsMixin, FileSystemAssertsMixin):

    PLAYBOOK = join(AnsiblePlayTestCase.FIXTURES_DIR, "install_gnome.yml")

    def test_setup_correctly(self):
        self.assert_file_exists(self.PLAYBOOK)

    def test_installs_gdm(self):
        remove_package("gdm", force=True)
        self.assert_package_not_installed("gdm")
        self.play()
        self.assert_package_installed("gdm")


if __name__ == "__main__":
    unittest.main()

