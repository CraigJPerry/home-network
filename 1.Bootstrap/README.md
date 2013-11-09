## Bootstrap Steps ##

1. Make auto install USB, CD or DVD
2. Launch the automated installation, which:
  1. Sets the hostname
  2. Installs Ansible
  3. Adds ansible in "pull mode" to crontab


## Remastering The Fedora DVD ##

We will install the "bootstrap node" using the vanilla
Fedora 19 DVD from the Fedora site. We will remaster the
ISO image to include our own kickstart file. You could
just as easily use the network install CD or whatever
but the DVD is what i already had laying around on my HD.

Finally, we'll copy the ISO onto a USB drive, although
burning an actual DVD would also be fine.

Download the installer ISO and extract it. The steps
i used on a linux box were:

    $ wget http://download.fedoraproject.org/pub/fedora/linux/releases/19/Fedora/x86_64/iso/Fedora-19-x86_64-DVD.iso
    $ sudo mount -o loop Fedora-19-x86_64-DVD.iso /mnt
    $ mkdir fedora19-bootstrap-node
    $ cp -a /mnt/. fedora19-bootstrap-node  # NB: The . is required
    $ sudo umount /mnt
    $ cp ~/d1.ks fedora-19-bootstrap-node
    $ cp ~/isolinux.cfg fedora-19-bootstrap-node

Make the iso image:
    $ cd fedora-19-bootstrap-node
    $ mkisofs -R -J -T -v -no-emul-boot -boot-load-size4 -boot-info-table -V "Fedora 19 x86_64" -b isolinux/isolinux.bin -c isolinux/boot.cat -o ~/f19-bootstrap-node.iso .

