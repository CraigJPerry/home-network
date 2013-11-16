#!/bin/bash
#
# Extract ISO file, insert kickstart, patch isolinux.cfg, rebuild iso
#

# Configuration
WORKING_DIR="/var/tmp/$(basename ${0} ".sh").$$.workdir"
SOURCE_ISO_MOUNTPOINT="/media/src-iso"
SHELL_CMD="bash"

function usage
{
    echo "usage: $(basename $0) [-h|--help] [-d|--dry-run] [-t|--tempdir dir] <distro-image.iso> <kickstart.ks>" > /dev/stderr
    exit ${1}
}

# Process command line options
ARGS=$(getopt -o hdt: -l "help,dry-run,tempdir:" -n "$(basename $0)" -- "${@}")
[[ ${?} -ne 0 ]] && usage 1

eval set -- "$ARGS"

while true; do
    case "${1}" in
        -h|--help )
            usage 0
        ;;
        -d|--dry-run )
            shift
            SHELL_CMD="cat -"
        ;;
        -t|--tempdir )
            shift
            WORKING_DIR=${1}
            shift
        ;;
        * )
            shift
            break
        ;;
    esac
done

# Basic sanity check of parameters
if [[ ${#} -ne 2 || ! -r ${1} || ! -r ${2} ]]; then
    usage 1
fi

# Determine attribute values
_SOURCE_ISO=${1}
_KICKSTART=${2}
_KS_FILE=$(basename ${_KICKSTART})
_DEST_ISO="${WORKING_DIR}/iso"
_VOLUME_NAME="$(isoinfo -d -i ${_SOURCE_ISO} | grep 'Volume id' | cut -f3- -d' ')"
_VOLUME_NAME_ISOLINUX=$(echo ${_VOLUME_NAME} | sed 's/ /\\\\\\x20/g')
_OUTPUT_NAME="$(basename ${_SOURCE_ISO} '.iso').patched.iso"
_ISOLINUX_CFG="${_DEST_ISO}/isolinux/isolinux.cfg"
_STANZA="label kickstart\n  menu label ^Kickstart\n  menu default\n  kernel vmlinuz\n  append initrd=initrd.img inst.stage2=hd:LABEL=${_VOLUME_NAME_ISOLINUX} ks=hd:LABEL=${_VOLUME_NAME_ISOLINUX}:/${_KS_FILE} text"

# Do the ISO patching
${SHELL_CMD} <<-COMMANDS
    # Mount source ISO
	sudo mkdir -p ${SOURCE_ISO_MOUNTPOINT}
	sudo mount -o loop,ro ${_SOURCE_ISO} ${SOURCE_ISO_MOUNTPOINT}

    # Extract ISO contents to temp location on disk
	mkdir -p ${_DEST_ISO}
	sudo cp -a ${SOURCE_ISO_MOUNTPOINT}/. ${_DEST_ISO}
	sudo chown -R ${UID} ${_DEST_ISO}
	chmod -R u+rw ${_DEST_ISO}

    # Inject kickstart file
	cp ${_KICKSTART} ${_DEST_ISO}/

    # Patch isolinux.cfg
    sed -i "s/^\s\+menu default//" ${_ISOLINUX_CFG}
    sed -i "s#^label linux#${_STANZA}\n\nlabel linux#" ${_ISOLINUX_CFG}

    # Build ISO image
	mkisofs -R -J -T -v -no-emul-boot -boot-load-size4 -boot-info-table -V "${_VOLUME_NAME}" -b isolinux/isolinux.bin -c isolinux/boot.cat -o "${WORKING_DIR}/${_OUTPUT_NAME}" ${_DEST_ISO}

    # Cleanup
	rm -rf ${_DEST_ISO}
	sudo umount ${SOURCE_ISO_MOUNTPOINT}
	sudo rmdir ${SOURCE_ISO_MOUNTPOINT}
COMMANDS

echo "Finished: ${WORKING_DIR}/${_OUTPUT_NAME}"

