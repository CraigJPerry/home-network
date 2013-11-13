#!/bin/bash
#
# Extract ISO file, insert kickstart, patch isolinux.cfg, rebuild iso
#


# --dry-run command line param does not action any changes
[[ "x${1}" == "x--dry-run" ]] && shift && DEFANG="echo "
CP="${DEFANG}/bin/cp"
WGET="${DEFANG}/usr/bin/wget"
SUDO="${DEFANG}/usr/bin/sudo"
MKISOFS="${DEFANG}/usr/bin/mkisofs"
MKDIR="${DEFANG}/usr/bin/mkdir"

function die
{
    echo "FATAL: ${@}" > /dev/stderr
    exit 1
}

function warn
{
    echo "WARNING: ${@}" > /dev/stderr
}



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
