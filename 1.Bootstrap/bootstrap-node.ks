# d3 Kickstart
# Craig J Perry, 3rd November 2013
#

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
volgroup d3-vgroot --pesize=4096 pv.11

# RAID 0 vgfast
part raid.21 --ondisk=sda --size=1 --grow --asprimary --fstype="mdmember"
part raid.22 --ondisk=sdb --size=1 --grow --asprimary --fstype="mdmember"
raid pv.20 --fstype="lvmpv" --level=1 --device=md2 raid.21 raid.22
volgroup d3-vgfast --pesize=4096 pv.20

# LVs
logvol swap  --fstype="swap" --size=4000 --name=swap --vgname=d3-vgroot
logvol /  --fstype="ext4" --size=15000 --label="d3-vgroot-lvroot" --name=root --vgname=d3-vgroot
logvol /var  --fstype="ext4" --size=5000 --label="d3-vgroot-lvvar" --name=var --vgname=d3-vgroot
logvol /home  --fstype="ext4" --size=10000 --label="d3-vgroot-lvhome" --name=home --vgname=d3-vgroot
logvol /srv --fstype="ext4" --size=20000 --label="d3-vgfast-lvsrv" --name=srv --vgname=d3-vgfast

# Users
auth --enableshadow --passalgo=sha512
rootpw --iscrypted $6$JSdgnAXgP16EA7MR$HQ4isREWMEgyKP3can3iaTr678f4HPgAhp3eUp7SAYBzSPevGyooLpQ0LapodSvXU27kvOJZA6Xt9M66//x5X/
group --gid=1000 --name="craig"
user --groups=craig,wheel --homedir=/home/craig --name=craig --password=$6$0L978wPXIBXN3yyU$WCkkYXz3jF21jo1/zvn/rBYiPjBTTQPZBAD4.VOyXFjFyM4z8EedAxUNQ1.pze64zUQy4c5QYgNofsW03eDPu/ --iscrypted --gecos="Craig Perry" --uid=1000

# Network information
network  --bootproto=dhcp --device=enp8s0 --activate --hostname="d3.local"

xconfig  --startxonboot

%packages
@base-x
@core
@firefox
@fonts
@gnome-desktop
@guest-desktop-agents
@hardware-support
@input-methods
@multimedia
@printing
@standard
@virtualization
git
ansible
%end

%post
echo "%wheel ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/wheel-nopass
chmod 0440 /etc/sudoers.d/wheel-nopass
%end

reboot --eject

