## Home Network ##

This repository contains the configuration data to automate buildout
and management of my home network using Kickstart and
[Ansible](www.ansibleworks.com).


### Repo Structure ###

I've gone with the [Ansible Best Practices](http://www.ansibleworks.com/docs/playbooks_best_practices.html)
layout plus a couple of extra dirs:

* ``plays/`` standalone or adhoc playbooks. Typically one-off
  procedures that would otherwise live in a shell script. Might
  relocate these under roles.
* ``tests/`` test cases for the playbooks
* ``utils/`` Some utilities for bootstrapping a new host (Redhat
  kickstart)

