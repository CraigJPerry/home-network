### Auto Installation Media via Kickstart ###

This should work with recent versions of Fedora, RHEL & Centos.

The ``inject-kickstart-to-iso.sh`` script captures the steps required
to remaster an ISO (netinst CD or full DVD, it doesn't matter) with a
kickstart file included and the boot menu updated to include a kickstart
install as the default option.

    $ inject-kickstart-to-iso.sh -h
    usage: inject-kickstart-to-iso.sh [-h|--help] [-d|--dry-run] [-t|--tempdir dir] <distro-image.iso> <kickstart.ks>

* ``--dry-run`` prints out the commands instead of running them
* ``--tempdir`` sets the working directory. Remastering DVD ISOs
  can take over 9Gb of disk space.

An example run:

    $ inject-kickstart-to-iso.sh Fedora-19-x86_64-DVD.iso d1.ks
    ... <output snipped> ...
    Finished: /var/tmp/inject-kickstart-to-iso.21167.workdir/Fedora-19-x86_64-DVD.patched.iso

You can either burn this image to a DVD or just copy it to a pen drive:

    $ dd if=Fedora-19-x86_64-DVD.patched.iso of=/dev/usbkey

As noted above, Fedora netinst CD or even RHEL / Centos images should
work here too.


### Alternative Installations ###

If you look at the example ``d1.ks`` kickstart file, it only installs
the minimal @core packages (empty %packages section implies only @core).

It's more about setting up the disk layout, hostname and installing
ansible to do the actual package installation & configuration.

See the [Network Device Naming](https://github.com/CraigJPerry/home-network/wiki/Networkdevicenaming)
page on the wiki if you're curious about the ``d1`` hostname.

If you do a similarly minimal installation via another method (even a
manual install) then so long as you install ansible the same way I do
here (in pull mode) you've completed all the steps to proceed to
2.Config

