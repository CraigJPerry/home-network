#!/bin/bash
#
# TITLE
#   gpsd-device-hook-selinux
# DESCRIPTION
#   Fix up gpsd selinux permissions to permit executing device hook
#


cd $(dirname $0)
/usr/sbin/semodule -i gpsd-device-hook-*.pp
