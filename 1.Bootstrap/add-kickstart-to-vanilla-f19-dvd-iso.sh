#!/bin/bash
#
# Extract ISO file, insert kickstart, patch isolinux.cfg, rebuild iso
#


# --dry-run command line param does not action any changes
[[ "x${1}" == "x--dry-run" ]] && shift && DEFANG="echo "
CP="${DEFANG}cp"
WGET="${DEFANG}wget"
SUDO="${DEFANG}sudo"
MKISOFS="${DEFANG}mkisofs"
MKDIR="${DEFANG}mkdir"
RMDIR="${DEFANG}rm -rf"
CHMOD="${DEFANG}chmod"

_TEMP_DIR="/var/tmp/$(basename ${0} ".sh").$$.workdir"
_TEMP_MOUNT="/media/src-iso"


function die
{
    echo "FATAL: ${@}" > /dev/stderr
    exit 1
}

function warn
{
    echo "WARNING: ${@}" > /dev/stderr
}

function usage
{
    cat - <<-CAT
	USAGE: $(basename ${0}) [OPTIONS] <iso_file>

	OPTIONS:
	    --dry-run    Just print out commands instead of executing them

	REQUIRED PARAMETERS:
	    iso_file     Path to valid Fedora / RedHat / Centos .ISO image

CAT
}

function mount_iso
{
    [[ ! -r ${1} ]] && die "Cannot read source iso \"${1}\""
    ${SUDO} mkdir -p ${_TEMP_MOUNT}
    ${SUDO} mount -o loop,ro $1 ${_TEMP_MOUNT}
}

function unmount_iso
{
    ${SUDO} umount ${_TEMP_MOUNT}
    ${SUDO} rmdir ${_TEMP_MOUNT}
}

function main
{
    cd $(dirname ${0})
    mount_iso ${1}
    ${MKDIR} $_TEMP_DIR
    ${SUDO} cp -a ${_TEMP_MOUNT}/. ${_TEMP_DIR}
    ${SUDO} chown -R ${UID} ${_TEMP_DIR}
    ${CHMOD} -R u+rw ${_TEMP_DIR}
    ${CP} d1.ks ${_TEMP_DIR}/
    ${CP} isolinux.cfg ${_TEMP_DIR}/isolinux/
    ${RMDIR} ${_TEMP_DIR}
    unmount_iso
}


case "${1}" in

    -h|--help )
        usage
    ;;

    * )
        main "${@}"
    ;;
esac

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
