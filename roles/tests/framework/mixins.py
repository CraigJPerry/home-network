#!/usr/bin/env python2.7


"""
TestCase mixins to give useful assertions.
   Craig J Perry <craigp84@gmail.com>
"""


import re
from os.path import exists, isfile, isdir, islink
from .helpers import _sudo


class FileSystemAssertsMixin(object):
    "Mix this class into your TestCase to get some file system assertions"

    def assert_file_exists(self, filepath, kind="any"):
        "Check if filepath exists and is a <file|dir|link>"

        self.assert_true(exists(filepath))

        if "file" in kind.lower():
            self.assert_true(isfile(filepath))
        elif "dir" in kind.lower():
            self.assert_true(isdir(filepath))
        elif "link" in kind.lower():
            self.assert_true(islink(filepath))

    def assert_file_doesnt_exist(self, filepath):
        "Confirm filepath doesn't exist"
        self.assert_true(not exists(filepath))

    def assert_file_contains(self, filepath, count, regex):
        "Check if filepath contains count occurances of regex"

        with open(filepath, "r") as fhandle:
            matches = sum(len(re.findall(regex, line)) for line in fhandle.xreadlines())
        self.assert_equal(count, matches)

    def assert_file_doesnt_contain(self, filepath, regex):
        "Check if filepath has 0 occurences of regex"
        return self.assert_file_contains(filepath, 0, regex)


class PackageAssertsMixin(object):
    "TestCase mixin giving assertions about the system packaging DB"

    def assert_package_not_installed(self, package_names):
        "Check if a package, or list of packages, are not installed"
        if not hasattr(package_names, '__iter__'):
            package_names = [package_names]

        for pkg in package_names:
            self.assert_true(not self._rpm_installed(pkg))

    def assert_package_installed(self, package_names):
        "Check if a package, or list of packages, are installed"

        if not hasattr(package_names, '__iter__'):
            package_names = [package_names]

        for pkg in package_names:
            self.assert_true(self._rpm_installed(pkg))

    def _rpm_installed(self, package_name):
        cmdline = ["/usr/bin/rpm", "-q", package_name]
        return _sudo(cmdline)

