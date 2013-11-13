#!/bin/bash
#
# Extract ISO file, insert kickstart, patch isolinux.cfg, rebuild iso
#


# Commands
FAKE_CP="echo cp"
REAL_CP="/bin/cp"
CP="${FAKE_CP}"

FAKE_WGET="echo wget"
REAL_WGET="/usr/bin/wget"
WGET="${FAKE_WGET}"

FAKE_SUDO="echo sudo"
REAL_SUDO="/usr/bin/sudo"
SUDO="${FAKE_SUDO}"

FAKE_MKISOFS="echo mkisofs"
REAL_MKISOFS="/usr/bin/mkisofs"
MKISOFS="${FAKE_MKISOFS}"

FAKE_MKDIR="echo mkdir"
REAL_MKDIR="/usr/bin/mkdir"
MKDIR="${FAKE_MKDIR}"

# From notes:
#    $ wget http://download.fedoraproject.org/pub/fedora/linux/releases/19/Fedora/x86_64/iso/Fedora-19-x86_64-DVD.iso
#    $ sudo mount -o loop Fedora-19-x86_64-DVD.iso /mnt
#    $ mkdir f19
#    $ cp -a /mnt/. f19  # NB: The . is required
#    $ sudo umount /mnt
#    $ cp ~/d1.ks f19
#    $ cp ~/isolinux.cfg f19
#    $ cd f19
#    $ mkisofs -R -J -T -v -no-emul-boot -boot-load-size4 -boot-info-table -V "Fedora 19 x86_64" -b isolinux/isolinux.bin -c isolinux/boot.cat -o ~/f19-d1.iso .
