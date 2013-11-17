## Testing Playbooks ##

All playbooks have associated tests. The only dependencies on your
development host are:

* Ansible, which is used to provision the VM each time it's installed
  afresh
* VirtualBox, used by Vagrant to host VMs
* Vagrant, which makes managing & provisioning VMs trivial


### Vagrant Virtual Machine ###

The ``Vagrantfile`` in this directory defines a machine for running
the tests:

1. Install vagrant + virtualbox
2. Run ``vagrant up`` from this directory

This will start and configure a VM with software dependencies installed
and shared access to this repository.


### Running Tests ###

To run all tests::

    [user@devbox ~]$ vagrant ssh
    [vagrant@vm ~]$ cd /home-network
    [vagrant@vm /home-network]$ python2.7 -m unittest discover

Run a single test::

    [vagrant@vm /home-network]$ python2.7 -m unittest tests.test_framework.TestFileSystemAssertsMixin.test_file_doesnt_contain


##  About Tests ##

I've chosen to try using only python2.7's builtin unittest module
(previously i was using nose) because it:

* Supported by all Python IDEs / environments
* Best understood by most Python developers in my experience
* Easiest to get help on for non-python developers

