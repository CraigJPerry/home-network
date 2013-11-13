## Bootstrap Steps ##

1. Make auto install USB, CD or DVD
2. Launch the automated installation, which:
  1. Sets the hostname
  2. Installs Ansible
  3. Adds ansible in "pull mode" to crontab


## Remastering The Fedora DVD ##

I've captured the steps for adding a kickstart file and a default
entry to the isolinux boot menu, in the ``inject-kickstart-to-iso.sh``
script:

    $ inject-kickstart-to-iso.sh -h
    usage: inject-kickstart-to-iso.sh [-h|--help] [-d|--dry-run] [-t|--tempdir dir] <distro-image.iso> <kickstart.ks>

    $ inject-kickstart-to-iso.sh Fedora-19-x86_64-DVD.iso d1.ks
    ... <output snipped> ...
    Finished: /var/tmp/inject-kickstart-to-iso.21167.workdir/Fedora-19-x86_64-DVD.patched.iso

You can either burn this image to a DVD or just copy it to a pen drive.

## Installation ##

Boot the DVD / pen drive and wait until it's complete.

The core installation DVD functionality remains intact, there's
now an extra menu option (the default) to use a kickstart file.

This means the same DVD can still be used for other installs, the
installation should be a "minimal install" anyway, we want all
configuration to be tracked in ansible.

