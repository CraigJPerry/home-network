## Testing Playbooks ##

All playbooks have associated tests. The only dependencies on your
development host are:

* Ansible, which is used to provision the VM each time it's installed
  afresh. See the provisioning role for more details.
* VirtualBox, used by Vagrant to host VMs
* Vagrant, which makes managing & provisioning VMs trivial


### Getting Started with Vagrant ###

The ``Vagrantfile`` in this directory defines a machine for running
the tests:

1. Install vagrant + virtualbox
2. Run ``vagrant up`` from this directory

This will start and configure a VM with software dependencies installed
and shared access to this repository.

To login, run ``vagrant ssh``.

Run ``vagrant suspend`` when you're finished. To resume development,
just do a ``vagrant up`` again.

If the VM is ever broken, or you just want a fresh start, do a
``vagrant destroy`` to blast it away followed by a ``vagrant up`` to
install a fresh virtual machine & provision for testing.

#### Shared Folder ####

The entire repo is visible inside the virtual machine under
``/home-network/``. Any changes made in your editor on your development
host are immediately reflected inside the VM.

### Running Tests ###

Some tests should run as root to accurately replicate the playbook's
intended use case, others should run as a non-root user with sudo
priveleges.

To run all tests::

    [user@devbox ~]$ vagrant ssh
    [vagrant@vm ~]$ cd /home-network
    [vagrant@vm home-network]$ sudo python -m unittest discover && python -m unittest discover

Run a single test::

    [vagrant@vm /home-network]$ python2.7 -m unittest tests.test_framework.TestFileSystemAssertsMixin.test_file_doesnt_contain


##  About Tests ##

I've chosen to try using only python2.7's builtin unittest module
(previously i was using nose) because it's:

* Supported by all Python IDEs / environments
* Best understood by most Python developers in my experience
* Easiest to get help on for non-python developers

