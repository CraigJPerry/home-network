#version=DEVEL
#
# v1 Kickstart
# Craig J Perry, 8th November 2013
#
# This is a minimal install, package selection is handled
# post-reboot by ansible config management. This ks file
# defines:
#  a) disk layout, 2x 8Gb sliced up as:
#    1) /boot, 128M RAID1 ext4
#    2) pv.11, 6Gb RAID1 LVM PV (/)
#    3) pv.20, Remainder RAID0 LVM PV (/scratch)
#  b) Hostname (with F19 bug workaround, see %post)
#  c) Root account with default password (changed on first reboot)
#

cdrom

lang en_GB.UTF-8
keyboard --vckeymap=uk --xlayouts='gb'
timezone Europe/London --isUtc

zerombr
clearpart --all --initlabel --drives=sda,sdb
ignoredisk --only-use=sda,sdb
# BUG: Only installs on sda
bootloader --location=mbr --driveorder=sda,sdb

# /boot
part raid.01 --ondisk=sda --maxsize=128 --size=128 --asprimary --fstype="mdmember"
part raid.02 --ondisk=sdb --maxsize=128 --size=128 --asprimary --fstype="mdmember"
raid /boot --fstype=ext4 --level=1 --device=0 raid.01 raid.02

# RAID 1 vgroot
part raid.11 --ondisk=sda --size=6000 --asprimary --fstype="mdmember"
part raid.12 --ondisk=sdb --size=6000 --asprimary --fstype="mdmember"
raid pv.11 --fstype="lvmpv" --level=1 --device=1 raid.11 raid.12
volgroup v1-vgroot --pesize=4096 pv.11

# RAID 0 vgfast
part raid.21 --ondisk=sda --size=1 --grow --asprimary --fstype="mdmember"
part raid.22 --ondisk=sdb --size=1 --grow --asprimary --fstype="mdmember"
raid pv.20 --fstype="lvmpv" --level=0 --device=2 raid.21 raid.22
volgroup v1-vgfast --pesize=4096 pv.20

# LVs
logvol swap  --fstype="swap" --size=512 --name=swap --vgname=v1-vgroot
logvol /  --fstype="ext4" --size=5000 --label="v1-vgroot-lvroot" --name=root --vgname=v1-vgroot
logvol /scratch --fstype="ext4" --size=512 --label="v1-vgfast-lvsrv" --name=srv --vgname=v1-vgfast

# Users
auth --enableshadow --passalgo=sha512
rootpw --iscrypted $6$JSdgnAXgP16EA7MR$HQ4isREWMEgyKP3can3iaTr678f4HPgAhp3eUp7SAYBzSPevGyooLpQ0LapodSvXU27kvOJZA6Xt9M66//x5X/

# Network information
network --bootproto=dhcp --device=eth0 --activate
# BUG: Fedora 19 manual workaround in %post below
network --hostname=v1.local

xconfig  --startxonboot

# No packages specified here (@core implied) as we want a
# minimal install. Ansible will handle packages post-install
%packages
%end

%post

# Workaround https://bugzilla.redhat.com/show_bug.cgi?id=981934
echo "v1.local" > /etc/hostname
echo "HOSTNAME=\"v1.local\"" > /etc/sysconfig/network

yum -y install git ansible

# Attempt to install ansible-pull mode, every 5 mins after reboot
echo "*/5 * * * * root ansible-pull --purge -U https://github.com/CraigJPerry/home-network -d home-network -i hosts-production plays/install-pull-mode.yml > /tmp/install-pull-mode.cron 2>&1" > /etc/cron.d/ansible-pull-install

%end

shutdown

