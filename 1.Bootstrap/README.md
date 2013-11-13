## Bootstrapping A Network ##

Buildout of the network is in 2 stages:

1. Install a *bootstrap* or *seed* host. This should use an automated
   installation method. I've chosen kickstart since i'm using Fedora.
2. Various services are installed on the first node, such as a cobbler
   instance to allow network install of further virtual machines,
   phyiscal nodes and even other OSs.


### Auto Installation Media via Kickstart ###

I'm using a DVD ISO written to a USB pendrive. No reason you couldn't
use a CD / DVD instead.

Download a vanilla source ISO. I'm using Fedora 19, but the script i've
written should work with other versions. It should even work with other
Redhat derived distributions such as RHEL, Centos & Scientific.

I've captured the steps for adding a kickstart file and a default
entry to the isolinux boot menu, in the ``inject-kickstart-to-iso.sh``
script:

    $ inject-kickstart-to-iso.sh -h
    usage: inject-kickstart-to-iso.sh [-h|--help] [-d|--dry-run] [-t|--tempdir dir] <distro-image.iso> <kickstart.ks>

    $ inject-kickstart-to-iso.sh Fedora-19-x86_64-DVD.iso d1.ks
    ... <output snipped> ...
    Finished: /var/tmp/inject-kickstart-to-iso.21167.workdir/Fedora-19-x86_64-DVD.patched.iso

You can either burn this image to a DVD or just copy it to a pen drive.


### Installation ###

Boot the DVD / pen drive and wait until it's complete.

The core installation DVD functionality remains intact, there's
now an extra menu option (the default) to use a kickstart file.

This means the same DVD can still be used for other installs, the
installation should be a "minimal install" anyway, we want all
configuration to be tracked in ansible.


### Alternative Installations ###

If you look at the example ``d1.ks`` kickstart file, it only installs
the minimal @core packages (empty %packages section implies only @core).
It's more about setting up the disk layout, hostname and installing
ansible to do the actual package installation & configuration.

If you do a similarly minimal installation via another method (even a
manual install) then so long as you install ansible the same way we do
here (in pull mode) you've completed all the steps to proceed to
2.Config

