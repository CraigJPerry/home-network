## Home Network ##

This repository captures the configuration data to
automate buildout and management of a small network;
my home network to be exact!

## Why? ##

I'm an ops guy at heart, it feels right to apply best
practice even at home.

It does make things quite nice, e.g. taking a new laptop
home, network booting it and 20 mins later having
everything installed and ready to go, just the way i like
it, with access to my data is really nice.

More practically, being able to spin up new virtual
machine instances in my own "private cloud" is quite
handy for side projects in my line of work.

Really, it all stems from the fact that I don't want to
lose any of my data (pictures, documents etc.) and this
is easier to do when the network's all cleanly setup.

## How Does It Work? ##

I have this git repo (replicated in multiple places -
a benefit of distributed version control systems!)
which contains all the configuration and documentation.

I use [Ansible](http://www.ansibleworks.com) configuration
management software to automatically apply appropriate
configuration to the nodes where ansible will run.

Some nodes such as my mobile phone don't support this
approach. Special cases are inevitable but are well
documentated and automated where possible.

## Can I Reuse This? ##

Yes! You'll want to alter some of the configuration but
definitely, just fork this repo and crack on. Everything's
documented. See the Getting Started section, it's pretty
easy.

### Things You Should Know ###

Everything is reconfigurable, and easily, with full tracked
history of changes complete with easy roll-backs.

This said, my configuration makes some decisions you may not
want to keep:

* I use only IPv6, with automatic link-local addressing
  although this is more just for the experience than anything
  else. It's trivial to re-introduce IPv4 with link-local
  addresses (the auto assigned 169.254.0.0/16 range).
* I use mdns (zeroconf / bonjour) for network naming
  rather than having a box on all the time to drive DNS.
  I'm energy efficient like that...

## Getting Started ##

Fork this repo.

1. Make sure the core network backbone is in place. In my
   case that's as simple as:
1.1 Ensure my internet router is wired up correctly to hosts
1.2 DHCP is turned off
1.3 A WiFi network configured
1.4 IPv6 enabled (LAN side only, since my ISP doesn't
    support IPv6 yet)
2. Have an idea of how you want your hardware to be used
2.1 Select the first node to re-install, the bootstrap
    node responsible for providing various key network
    services like automated remote installation. The
    rest of the network builds out from this node.
    
    These services are all containerised in virtual machines
    so they can trivially be migrated to other hosts in
    future.

    This node runs Fedora Linux in my configuration since
    it also doubles up as a desktop and i've recently
    switched from Ubuntu for my desktop of choice
2.2 Make the install USB/CD/DVD for the first node and kick
    off the automated installation
3. Ansible will now apply the configuration to this node
   which involves bringing up various virtual machines. One
   of these is a Cobbler network installation service. It
   makes jumpstarting other installs over the network (and
   building virtual machines) very fast and easy. It also
   manages updates for other nodes and caches downloaded
   packages locally for speed. Much nicer than making lots
   of USB boot drives to install other systems.
4. Edit the ansible playbooks to suit your desired state
   and kickstart other hosts & virtual machines to build
   out your new network

