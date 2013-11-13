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
ISOINFO="${DEFANG}isoinfo"

_TEMP_DIR="/var/tmp/$(basename ${0} ".sh").$$.workdir"
_ISO_DIR="${_TEMP_DIR}/iso"
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

function write_iso
{
    VOLUME_NAME="$(${ISOINFO} -d -i ${1} | grep 'Volume id' | cut -f3- -d' ')"
    OUTPUT_NAME="$(basename ${1} '.iso').patched.iso"
    ${MKISOFS} -R -J -T -v -no-emul-boot -boot-load-size4 -boot-info-table -V "${VOLUME_NAME}" -b isolinux/isolinux.bin -c isolinux/boot.cat -o "${_TEMP_DIR}/${OUTPUT_NAME}" ${_ISO_DIR}
}

function main
{
    cd $(dirname ${0})
    mount_iso ${1}
    ${MKDIR} -p ${_ISO_DIR}
    ${SUDO} cp -a ${_TEMP_MOUNT}/. ${_ISO_DIR}
    ${SUDO} chown -R ${UID} ${_ISO_DIR}
    ${CHMOD} -R u+rw ${_ISO_DIR}
    ${CP} d1.ks ${_ISO_DIR}/
    ${CP} isolinux.cfg ${_ISO_DIR}/isolinux/
    write_iso ${1}
    ${RMDIR} ${_ISO_DIR}
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

