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
    $ cp ~/bootstrap-node.ks fedora-19-bootstrap-node
    $ vi fedora19-bootstrap-node/isolinux/isolinux.cfg

I added the below stanza to the isolinux.cfg file:

    label kickstart
      menu label Kickstart Bootstrap Node with F19
      kernel vmlinuz
      append initrd=initrd.img inst.stage2=hd:LABEL=Fedora\x2019\x20x86_64 text ks=cdrom:/bootstrap-node.ks

And i changed the default line at the top:

    default kickstart

Make the iso image:

    $ sudo mkisofs -o ~/f19-bootstrap-node.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -R -J -v -T .

