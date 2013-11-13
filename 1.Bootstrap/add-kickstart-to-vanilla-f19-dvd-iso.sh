#!/bin/bash
#
# Extract _ISO file, insert kickstart & isolinux.cfg, rebuild iso
#

# CONFIGURATION
WORKING_DIR="/var/tmp/$(basename ${0} ".sh").$$.workdir"
SOURCE_ISO_MOUNTPOINT="/media/src-iso"
# END CONFIGURATION

function usage
{
    echo "usage: $(basename $0) [-h|--help] [--dry-run] [-t|--tempdir dir] <distro-image.iso> <kickstart.ks>" > /dev/stderr
    exit ${1}
}

# Process & remove options
if [[ "x${1}" == "x--help" || "x${1}" == "x-h" ]]; then
    usage 0
elif [[ "x${1}" == "x--tempdir" || "x${1}" == "x-t" ]]; then
    WORKING_DIR=${1}
    shift
elif [[ "x${1}" == "x--dry-run" ]]; then
    shift
    SHELL_CMD="cat -"
else
    SHELL_CMD="bash"
fi

# Check parameters
if [[ ${#} -ne 2 || ! -r ${1} || ! -r ${2} ]]; then
    usage 1
fi

# Calculated values
_ISO_DIR="${WORKING_DIR}/iso"
_THIS_DIR="$(dirname ${0})"
_VOLUME_NAME="$(isoinfo -d -i ${1} | grep 'Volume id' | cut -f3- -d' ')"
_OUTPUT_NAME="$(basename ${1} '.iso').patched.iso"

# Do the patching
${SHELL_CMD} <<-COMMANDS
	cd ${_THIS_DIR}
	sudo mkdir -p ${SOURCE_ISO_MOUNTPOINT}
	sudo mount -o loop,ro $1 ${SOURCE_ISO_MOUNTPOINT}
	mkdir -p ${_ISO_DIR}
	sudo cp -a ${WORKING_DIR}/. ${_ISO_DIR}
	sudo chown -R ${UID} ${_ISO_DIR}
	chmod -R u+rw ${_ISO_DIR}
	cp d1.ks ${_ISO_DIR}/
	cp isolinux.cfg ${_ISO_DIR}/isolinux/
	mkisofs -R -J -T -v -no-emul-boot -boot-load-size4 -boot-info-table -V "${_VOLUME_NAME}" -b isolinux/isolinux.bin -c isolinux/boot.cat -o "${WORKING_DIR}/${_OUTPUT_NAME}" ${_ISO_DIR}
	rm -rf ${_ISO_DIR}
	sudo umount ${SOURCE_ISO_MOUNTPOINT}
	sudo rmdir ${SOURCE_ISO_MOUNTPOINT}
COMMANDS

