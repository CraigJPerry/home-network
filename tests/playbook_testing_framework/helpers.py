#!/usr/bin/env python2.7


"""
Helper functions to setup / teardown test environment.
   Craig J Perry <craigp84@gmail.com>
"""


import os
import subprocess
from tempfile import TemporaryFile


class SudoError(Exception):
    "Sudo returned an unexpected return code"
    pass


def _sudo(cmdline, expected_return_codes=[]):
    """Run cmdline via sudo.

    Return True if return code 0.
    False if return code in expected_return_codes.
    Any other return code raises SudoError"""

    if not hasattr(cmdline, '__iter__'):
        cmdline = [cmdline]

    if not expected_return_codes:
        expected_return_codes = [1]

    if not os.geteuid() == 0:
        cmdline = ["/usr/bin/sudo"] + cmdline

    with TemporaryFile() as stdout_stderr:
        try:
            return_code = subprocess.check_call(cmdline, stdout=stdout_stderr, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            if ex.returncode in expected_return_codes:
                return False
            else:
                stdout_stderr.seek(0)
                output = stdout_stderr.read()
                msg = "Failed to run command [%s] because [%s]" % (
                        cmdline, output.replace("\n", " "))
                raise SudoError(msg)
        else:
            return True


def install_package(package_names):
    "Yum install package(s)"
    if not hasattr(package_names, '__iter__'):
        package_names = [package_names]

    cmdline = ["/usr/bin/yum", "-y", "install"] + package_names
    return _sudo(cmdline)


def remove_package(package_names, force=False):
    "Return True if uninstalled, False if already uninstalled"
    if not hasattr(package_names, '__iter__'):
        package_names = [package_names]

    cmdline = ["/usr/bin/rpm", "-e"] + package_names
    if force:
        cmdline.append("--nodeps")

    return _sudo(cmdline)


def remove_user(usernames):
    "Return True if removed, False if wasn't present already"
    if not hasattr(usernames, '__iter__'):
        usernames = [usernames]

    cmdline = ["/sbin/userdel"] + usernames
    return _sudo(cmdline, expected_return_codes = [6])


def add_user(username):
    "Convenience func to add user account"
    cmdline = ["/sbin/useradd", username]
    return _sudo(cmdline, expected_return_codes = [4, 9])

