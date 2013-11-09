#version=DEVEL
#
# d1 Kickstart
# Craig J Perry, 8th November 2013
#
# This is a minimal install, package selection is handled
# post-reboot by ansible config management. This ks file
# defines:
#  a) disk layout, 2x 500Gb sliced up as:
#    1) /boot, 256M RAID1 ext4
#    2) pv.11, 200Gb RAID1 LVM PV (/, /var, /home etc.)
#    3) pv.20, Remainder RAID0 LVM PV (/scratch)

cdrom

lang en_GB.UTF-8
keyboard --vckeymap=uk --xlayouts='gb'
timezone Europe/London --isUtc

zerombr
clearpart --all --initlabel --drives=sda,sdb
ignoredisk --only-use=sda,sdb
bootloader --location=mbr --driveorder=sda,sdb

# /boot
part raid.01 --ondisk=sda --maxsize=256 --size=256 --asprimary --fstype="mdmember"
part raid.02 --ondisk=sdb --maxsize=256 --size=256 --asprimary --fstype="mdmember"
raid /boot --fstype=ext4 --level=1 --device=md0 raid.01 raid.02

# RAID 1 vgroot
part raid.11 --ondisk=sda --size=200000 --asprimary --fstype="mdmember"
part raid.12 --ondisk=sdb --size=200000 --asprimary --fstype="mdmember"
raid pv.11 --fstype="lvmpv" --level=1 --device=md1 raid.11 raid.12
volgroup d1-vgroot --pesize=4096 pv.11

# RAID 0 vgfast
part raid.21 --ondisk=sda --size=1 --grow --asprimary --fstype="mdmember"
part raid.22 --ondisk=sdb --size=1 --grow --asprimary --fstype="mdmember"
raid pv.20 --fstype="lvmpv" --level=0 --device=md2 raid.21 raid.22
volgroup d1-vgfast --pesize=4096 pv.20

# LVs
logvol swap  --fstype="swap" --size=4000 --name=swap --vgname=d1-vgroot
logvol /  --fstype="ext4" --size=15000 --label="d1-vgroot-lvroot" --name=root --vgname=d1-vgroot
#logvol /var  --fstype="ext4" --size=10000 --label="d1-vgroot-lvvar" --name=var --vgname=d1-vgroot
#logvol /home  --fstype="ext4" --size=30000 --label="d1-vgroot-lvhome" --name=home --vgname=d1-vgroot
logvol /scratch --fstype="ext4" --size=30000 --label="d1-vgfast-lvsrv" --name=srv --vgname=d1-vgfast

# Users
auth --enableshadow --passalgo=sha512
rootpw --iscrypted $6$JSdgnAXgP16EA7MR$HQ4isREWMEgyKP3can3iaTr678f4HPgAhp3eUp7SAYBzSPevGyooLpQ0LapodSvXU27kvOJZA6Xt9M66//x5X/
group --gid=1000 --name="craig"
user --groups=craig,wheel --homedir=/home/craig --name=craig --password=$6$0L978wPXIBXN3yyU$WCkkYXz3jF21jo1/zvn/rBYiPjBTTQPZBAD4.VOyXFjFyM4z8EedAxUNQ1.pze64zUQy4c5QYgNofsW03eDPu/ --iscrypted --gecos="Craig Perry" --uid=1000

# Network information
network  --bootproto=dhcp --device=eth0 --activate --hostname="d1.local"
network  --bootproto=dhcp --device=enp8s0 --activate --hostname="d1.local"

xconfig  --startxonboot

# No packages specified here, we want a minimal install, ansible
# will handle installing the right packages later
%packages
%end

%post
echo "%wheel ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/wheel-nopass
chmod 0440 /etc/sudoers.d/wheel-nopass

# Depending on the install media used, not all packages are
# guaranteed to be present. Easy workaround is just to install
# over the network at the end of the installation process.
yum -y update
yum -y install git
yum -y install ansible
yum -y install avahi avahi-tools
%end

reboot --eject

