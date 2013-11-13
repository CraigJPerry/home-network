## Bootstrapping A Network ##

Buildout of the network is in 2 stages:

1. Install a *bootstrap* or *seed* host. This should use an automated
   installation method. I've chosen kickstart since i'm using Fedora.
2. Various services are installed on the first node, such as a cobbler
   instance to allow network install of further virtual machines,
   phyiscal nodes and other OSs.


### Auto Installation Media via Kickstart ###

I write a DVD ISO to a USB pendrive. You could burn a CD / DVD instead.

Download a vanilla source ISO. I'm using Fedora 19 (either netinst CD or
full DVD will work). The script should work with other versions of Fedora.
It should even work with other Redhat derived distributions such as RHEL,
Centos & Scientific, without any changes.

    $ inject-kickstart-to-iso.sh -h
    usage: inject-kickstart-to-iso.sh [-h|--help] [-d|--dry-run] [-t|--tempdir dir] <distro-image.iso> <kickstart.ks>

The ``--dry-run`` option prints out the commands instead of running
them. The ``--tempdir`` sets the working directory, you can need almost
10GB of space in the case of using a DVD.

    $ inject-kickstart-to-iso.sh Fedora-19-x86_64-DVD.iso d1.ks
    ... <output snipped> ...
    Finished: /var/tmp/inject-kickstart-to-iso.21167.workdir/Fedora-19-x86_64-DVD.patched.iso

You can either burn this image to a DVD or just copy it to a pen drive.


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

